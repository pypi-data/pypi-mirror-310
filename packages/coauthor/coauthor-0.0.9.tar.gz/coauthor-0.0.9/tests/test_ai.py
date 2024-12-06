import os
import tempfile
import logging
import pytest
from coauthor.utils.logger import Logger
from unittest.mock import patch, mock_open, MagicMock
from coauthor.utils.config import get_config
from coauthor.modules.ai import (
    process_file_with_openai_agent,
    process_with_openai_agent,
    load_system_message,
    prompt_template_path,
    user_template_path,
)
import yaml
import jinja2
import openai


def get_pong_config():
    config_path = os.path.join(os.path.dirname(__file__), "data", "coauthor_task_pong.yml")
    with open(config_path, "r") as file:
        task = yaml.safe_load(file)
    return task


def test_process_with_openai_agent_system_message_template():
    """
    Test the `process_with_openai_agent` function using a system message from a template file.

    It simulates the OpenAI agent being set up to always respond with "pong", ensuring that the
    system message is correctly loaded from a file and used as expected.
    """
    config = get_pong_config()
    config["current-workflow"] = config["workflows"][0]
    config["current-task"] = config["current-workflow"]["tasks"][0]
    task = config["current-task"]
    system_message = task["system"]
    del task["system"]

    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")

    with tempfile.TemporaryDirectory() as temp_config_dir:
        config["jinja"] = {"search_path": temp_config_dir}
        path_template = prompt_template_path(config, "system.md")
        path_system_message = os.path.join(temp_config_dir, path_template)
        os.makedirs(os.path.dirname(path_system_message), exist_ok=True)
        with open(path_system_message, "w", encoding="utf-8") as file1:
            logger.info(f"System message path: {path_system_message}")
            logger.info(f"System message: {system_message}")
            file1.write(system_message)
        with patch("coauthor.modules.ai.create_chat_completion", return_value="pong"):
            response = process_with_openai_agent(config, logger)
        assert response == "pong"


def test_process_with_openai_agent_user_message_template():
    """
    Test the `process_with_openai_agent` function using a user message from a Jinja template file.

    This test demonstrates the flexibility of using Jinja templating to create user messages,
    with access to configuration variables that provide access to tasks within workflows.

    It simulates the OpenAI agent being set up to always respond with "pong".
    """
    config = get_pong_config()
    config["current-workflow"] = config["workflows"][0]
    config["current-task"] = config["current-workflow"]["tasks"][0]
    task = config["current-task"]

    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")

    with tempfile.TemporaryDirectory() as temp_config_dir:

        # Create user template
        config["jinja"] = {"search_path": temp_config_dir}
        path_template = user_template_path(config)
        path_user_message = os.path.join(temp_config_dir, path_template)
        user_message = "User template for {{ config['current-task']['id'] }}"
        os.makedirs(os.path.dirname(path_user_message), exist_ok=True)
        with open(path_user_message, "w", encoding="utf-8") as file1:
            logger.info(f"User message path: {path_user_message}")
            logger.info(f"User message: {user_message}")
            file1.write(user_message)

        # Create a file and process with AI
        with tempfile.TemporaryDirectory() as temp_watch_dir:
            task["path-modify-event"] = os.path.join(temp_watch_dir, "whatever.md")
            with open(task["path-modify-event"], "w", encoding="utf-8") as file1:
                file1.write("File content")

            with patch("coauthor.modules.ai.create_chat_completion", return_value="pong"):
                response = process_with_openai_agent(config, logger)
            assert response == "pong"


def test_process_with_openai_agent_user_message_template_missing():
    """
    Test the `process_with_openai_agent` function when the user message template is missing.

    It simulates the OpenAI agent being set up to always respond with "pong".
    """
    config = get_pong_config()
    config["current-workflow"] = config["workflows"][0]
    config["current-task"] = config["current-workflow"]["tasks"][0]

    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a user template
        config["jinja"] = {"search_path": temp_dir}
        path_user_template = os.path.join(temp_dir, user_template_path(config))
        user_message = "User template for {{ config['current-task']['id'] }}"
        os.makedirs(os.path.dirname(path_user_template), exist_ok=True)
        with open(path_user_template, "w", encoding="utf-8") as file1:
            logger.info(f"User message path: {path_user_template}")
            logger.info(f"User message: {user_message}")
            file1.write(user_message)
        with patch("coauthor.modules.ai.create_chat_completion", return_value="pong"):
            response = process_with_openai_agent(config, logger)
        assert response == "pong"


def test_process_with_openai_agent_config_missing_system_template():
    """
    Test `process_with_openai_agent` function with configuration missing
    system template "ping-workflow/ping-task/system.md".

    Should throw a jinja2.exceptions.TemplateNotFound error.
    """
    config = get_pong_config()
    config["current-workflow"] = config["workflows"][0]
    config["current-task"] = config["current-workflow"]["tasks"][0]
    task = config["current-task"]
    del task["system"]
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")

    with pytest.raises(ValueError) as excinfo:
        process_with_openai_agent(config, logger)

    assert 'An AI task should have a key "system" or a template with path "ping-workflow/ping-task/system.md"' in str(
        excinfo.value
    )


def test_load_system_message_exception_handling():
    """
    Test `load_system_message` function to handle exceptions during file reading.

    Ensures that an IOError is raised and logged appropriately when the file cannot be read.
    """
    mock_logger = MagicMock()
    agent_system_path = "fake_path"

    with patch("coauthor.modules.ai.os.path.exists", return_value=True):
        with patch("builtins.open", mock_open()) as mocked_open:
            mocked_open.side_effect = IOError("Mocked IOError")

            with pytest.raises(IOError):
                load_system_message(agent_system_path, mock_logger)

            mock_logger.error.assert_called_once_with("Error reading system message file: Mocked IOError")
