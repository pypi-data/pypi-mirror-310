import jinja2
import os
from coauthor.utils.config import get_jinja_config
from coauthor.utils.git import get_git_diff
from coauthor.utils.jinja_filters import select_task, get_task_attribute


def render_template_to_file(task, template, path, config, logger):
    content = render_template(task, template, config, logger)
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def search_path_directories(search_path):
    # Return a list of directory search_path and all its subdirectories
    directories = []
    for root, dirs, files in os.walk(search_path):
        directories.append(root)
    return directories


def template_exists(task, template, config, logger):
    config = get_jinja_config(config)
    search_paths = search_path_directories(config["search_path"])
    template_loader = jinja2.FileSystemLoader(searchpath=search_paths)
    templates = template_loader.list_templates()
    if template in templates:
        return True
    logger.debug(f"Template {template} not found!")
    return False


def render_template(task, template_path, config, logger):
    logger.debug(f"Render template {template_path} for task {task['id']}")
    jinja_config = get_jinja_config(config)
    search_paths = search_path_directories(jinja_config["search_path"])
    template_loader = jinja2.FileSystemLoader(searchpath=search_paths)
    templates = template_loader.list_templates()
    logger.debug(f"templates: {templates}")
    if "custom_delimiters" in jinja_config:
        logger.debug("Creating Jinja environment using custom delimiters")
        custom_delimiters = jinja_config["custom_delimiters"]
        template_env = jinja2.Environment(
            loader=template_loader,
            block_start_string=custom_delimiters.get("block_start_string", "{%"),
            block_end_string=custom_delimiters.get("block_end_string", "%}"),
            variable_start_string=custom_delimiters.get("variable_start_string", "{{"),
            variable_end_string=custom_delimiters.get("variable_end_string", "}}"),
            comment_start_string=custom_delimiters.get("comment_start_string", "{#"),
            comment_end_string=custom_delimiters.get("comment_end_string", "#}"),
        )
    else:
        template_env = jinja2.Environment(loader=template_loader)
    template_env.filters["include_file_content"] = include_file_content
    template_env.filters["get_git_diff"] = get_git_diff
    template_env.filters["file_exists"] = file_exists
    template_env.filters["select_task"] = select_task
    template_env.filters["get_task_attribute"] = get_task_attribute

    logger.debug(f"Get Jinja template: {template_path}")
    template = template_env.get_template(template_path)
    context = {"config": config, "task": task, "workflow": config["current-workflow"]}
    return template.render(context)


def render_content(task, template_string, config, logger):
    logger.debug(f"Render content for task {task['id']}")
    jinja_config = get_jinja_config(config)

    if "custom_delimiters" in jinja_config:
        logger.debug("Creating Jinja environment using custom delimiters")
        custom_delimiters = jinja_config["custom_delimiters"]
        template_env = jinja2.Environment(
            block_start_string=custom_delimiters.get("block_start_string", "{%"),
            block_end_string=custom_delimiters.get("block_end_string", "%}"),
            variable_start_string=custom_delimiters.get("variable_start_string", "{{"),
            variable_end_string=custom_delimiters.get("variable_end_string", "}}"),
            comment_start_string=custom_delimiters.get("comment_start_string", "{#"),
            comment_end_string=custom_delimiters.get("comment_end_string", "#}"),
        )
    else:
        template_env = jinja2.Environment()

    template_env.filters["include_file_content"] = include_file_content
    template_env.filters["get_git_diff"] = get_git_diff
    template_env.filters["file_exists"] = file_exists
    template_env.filters["select_task"] = select_task
    template_env.filters["get_task_attribute"] = get_task_attribute

    template = template_env.from_string(template_string)
    context = {"config": config}
    return template.render(context)


def include_file_content(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def file_exists(path):
    return os.path.exists(path)
