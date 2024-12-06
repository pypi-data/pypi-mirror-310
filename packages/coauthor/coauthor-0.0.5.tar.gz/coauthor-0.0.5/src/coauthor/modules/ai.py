import os
import traceback
import yaml
import datetime
from openai import OpenAI
from coauthor.utils.match_utils import file_submit_to_ai, path_new_replace
from coauthor.utils.jinja import render_template, template_exists


def load_system_message(agent_system_path, logger):
    """Loads the system message from a string or a file."""
    logger.info(f"System message from file {agent_system_path}")
    if os.path.exists(agent_system_path):
        try:
            with open(agent_system_path, "r", encoding="utf-8") as file:
                system_message = file.read()
            logger.info(f"Loaded system message from file: {agent_system_path}")
            return system_message
        except Exception as error:
            logger.error(f"Error reading system message file: {error}")
            raise
    else:
        raise FileNotFoundError(f"The system path {agent_system_path} does not exist")


def write_response_to_yaml(config, messages, model, response, logger, duration=None):
    """Writes response data to respective markdown and YAML files."""
    task = config["current-task"]
    workflow = config["current-workflow"]
    coauthor_ai_log_dir = os.getenv("COAUTHOR_AI_LOG_DIR")
    if not coauthor_ai_log_dir:
        logger.debug("Environment variable COAUTHOR_AI_LOG_DIR not set")
        return

    counter_file_path = os.path.join(coauthor_ai_log_dir, ".ai-prompt-counter")
    if not os.path.exists(counter_file_path):
        message_id = 1
        with open(counter_file_path, "w", encoding="utf-8") as counter_file:
            counter_file.write(str(message_id))
    else:
        with open(counter_file_path, "r+", encoding="utf-8") as counter_file:
            message_id = int(counter_file.read())
            message_id += 1
            counter_file.seek(0)
            counter_file.write(str(message_id))

    # Create directory path for markdown files
    markdown_dir = os.path.join(coauthor_ai_log_dir, f"{workflow['name']}/{task['id']}")
    os.makedirs(markdown_dir, exist_ok=True)

    # Write each message to an individual markdown file
    for msg in messages:
        md_file_path = os.path.join(markdown_dir, f"{message_id}-{msg['role']}.md")
        with open(md_file_path, "w", encoding="utf-8") as md_file:
            md_file.write(msg["content"])
        logger.info(f"Message written to Markdown file: {md_file_path}")

    yaml_file_path = os.path.join(markdown_dir, f"{message_id}.yml")
    task["ai-log-file"] = yaml_file_path

    data = {
        "messages": [{"role": msg["role"], "tokens": len(msg["content"].split())} for msg in messages],  # Count words
        "model": model,
        "response": response,
        "task": task,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duration": duration,  # Add the duration to the data
    }
    try:
        with open(yaml_file_path, "w", encoding="utf-8") as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
        logger.info(f"Response written to YAML file: {yaml_file_path}")
    except Exception as error:
        logger.error(f"Error writing response to YAML file: {error}")
        raise


def create_chat_completion(config, client, messages, logger):
    """Create a chat completion using OpenAI client."""
    model = config["agent"]["model"]
    try:
        start_time = datetime.datetime.now()  # Record start time
        response = client.chat.completions.create(
            messages=messages,
            model=model,
        )
        end_time = datetime.datetime.now()  # Record end time
        duration = (end_time - start_time).seconds  # Calculate duration

        content = response.choices[0].message.content.strip()

        write_response_to_yaml(config, messages, model, content, logger, duration)

        if content.startswith("```") and content.endswith("```"):
            content_lines = content.splitlines()[1:-1]
            content = "\n".join(content_lines).strip()
        return content

    except Exception as error:
        logger.error(f"Error creating chat completion: {error}")
        logger.error(traceback.format_exc())
        raise


def prompt_template_path(config, filename):
    task = config["current-task"]
    workflow = config["current-workflow"]
    return f"{workflow['name']}/{task['id']}/{filename}"


def user_template_path(config, filename="user.md"):
    return prompt_template_path(config, filename)


def system_template_path(config, filename="system.md"):
    return prompt_template_path(config, filename)


def process_with_openai_agent(config, logger):
    """Submit content to OpenAI API for processing."""
    task = config["current-task"]
    logger.info(f"Processing content using AI for task {task['id']}")
    agent = config["agent"]
    logger.debug(f"agent: {agent}")

    if "api_key" in agent:
        api_key = agent["api_key"]
    else:
        api_key = os.getenv(agent["api_key_var"])
    if "api_url" in agent:
        api_url = agent["api_url"]
    else:
        api_url = os.getenv(agent["api_url_var"])

    client = OpenAI(
        api_key=api_key,
        base_url=api_url,
    )

    message_system_and_user = {}
    for system_or_user in ["system", "user"]:
        path_template = prompt_template_path(config, f"{system_or_user}.md")
        if template_exists(task, path_template, config, logger):
            message_system_and_user[system_or_user] = render_template(task, path_template, config, logger)
        elif system_or_user in task:
            message_system_and_user[system_or_user] = task[system_or_user]
        else:
            if "path-modify-event" in task and system_or_user == "user" and "user" not in task:
                logger.info(f"Using the file {task['path-modify-event']} as the user message")
                message_system_and_user[system_or_user] = file_submit_to_ai(config, logger)
            else:
                raise ValueError(
                    f'An AI task should have a key "{system_or_user}" or a template with path "{path_template}"'
                )

    # Log only the first line of the messages
    user_message = message_system_and_user["user"].splitlines()[0] if message_system_and_user["user"] else ""
    system_message = message_system_and_user["system"].splitlines()[0] if message_system_and_user["system"] else ""
    logger.debug(f"user_message: {user_message}")
    logger.debug(f"system_message: {system_message}")

    messages = [
        {
            "role": "system",
            "content": message_system_and_user["system"],
        },
        {"role": "user", "content": message_system_and_user["user"]},
    ]

    return create_chat_completion(config, client, messages, logger)


def process_file_with_openai_agent(config, logger):
    """Submit file to OpenAI API for processing."""
    task = config["current-task"]
    task["response"] = process_with_openai_agent(config, logger)
    return task["response"]
