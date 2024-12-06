import os
import yaml
import logging
from unittest.mock import patch, mock_open
from coauthor.modules.file_processor import regex_replace_in_file, pong
from coauthor.utils.logger import Logger
from unittest import mock


def get_config():
    config_path = os.path.join(os.path.dirname(__file__), "data", "coauthor-regex-replace.yml")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def test_regex_replace_in_file_changes_content():
    config = get_config()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    task["path-modify-event"] = "test.txt"
    test_content = "This is a test string with -> to be replaced."
    updated_content = "This is a test string with → to be replaced."
    with patch("builtins.open", mock_open(read_data=test_content)) as mock_file:
        assert open(task["path-modify-event"]).read() == test_content
        result = regex_replace_in_file(config, logger)
        assert result == True
        assert task["content"] == updated_content
        mock_file().write.assert_called()


def test_regex_replace_in_file_no_change():
    config = get_config()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    task["path-modify-event"] = "test.txt"
    test_content = "This is a test string with → already replaced."
    with patch("builtins.open", mock_open(read_data=test_content)) as mock_file:
        assert open(task["path-modify-event"]).read() == test_content
        result = regex_replace_in_file(config, logger)
        assert result == False
        assert "content" not in task
        mock_file().write.assert_not_called()


def test_regex_replace_in_file_with_capturing_groups():
    config = get_config()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    task["path-modify-event"] = "test.txt"
    test_content = "User: John_Doe, User: Jane_Doe"
    updated_content = "User: John Doe, User: Jane Doe"
    with patch("builtins.open", mock_open(read_data=test_content)) as mock_file:
        assert open(task["path-modify-event"]).read() == test_content
        result = regex_replace_in_file(config, logger)
        assert result == True
        assert task["content"] == updated_content
        mock_file().write.assert_called_once_with(updated_content)


def test_regex_replace_in_file_with_capturing_groups2():
    config = get_config()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    task["path-modify-event"] = "test.txt"
    test_content = "User: John_Doe, User: Jane_Doe"
    updated_content = "User: John Doe, User: Jane Doe"
    regex_replacements = [{"regex": r"User: (\w+)_(\w+)", "replace": r"User: \1 \2"}]
    with patch("builtins.open", mock_open(read_data=test_content)) as mock_file:
        assert open(task["path-modify-event"]).read() == test_content
        result = regex_replace_in_file(config, logger)
        assert result == True
        assert task["content"] == updated_content
        mock_file().write.assert_called_once_with(updated_content)


def test_pong():
    config = get_config()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    task["path-modify-event"] = "test.txt"
    test_content = "pong"
    mocked_open = mock_open(read_data=test_content)
    with mock.patch("builtins.open", mocked_open):
        pong(config, logger)
    mocked_open().write.not_called
    # mock_logger.info.assert_any_call("Running the pong file processor" + "mock_path")


def test_ping():
    config = get_config()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    test_content = "ping"
    mocked_open = mock_open(read_data=test_content)
    with mock.patch("builtins.open", mocked_open):
        task["path-modify-event"] = "mock_path"
        pong(config, logger)
    mocked_open().write.assert_called_once_with("pong")


def test_regex_replace_in_file_with_internal_regex():
    config = get_config()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    task["path-modify-event"] = "test.txt"
    test_content = "{{< line1\nline2>}}"
    updated_content = "{{< line1 line2>}}"
    with patch("builtins.open", mock_open(read_data=test_content)) as mock_file:
        assert open(task["path-modify-event"]).read() == test_content
        result = regex_replace_in_file(config, logger)
        assert result == True
        assert task["content"] == updated_content
        mock_file().write.assert_called_once_with(updated_content)


def test_file_open_mock():
    with patch("builtins.open", mock_open(read_data="data")) as mock_file:
        assert open("path/to/open").read() == "data"
