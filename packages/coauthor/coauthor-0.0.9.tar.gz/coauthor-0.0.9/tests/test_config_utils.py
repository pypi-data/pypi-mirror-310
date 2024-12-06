import logging
from coauthor.utils.config import get_config, get_config_path
from coauthor.utils.logger import Logger
import os


def test_get_config_path_returns_correct_coauthor_file():
    """
    Test that the `get_config_path` function correctly returns the file path
    of the '.coauthor.yml' file located in the current project root directory.
    """
    file_path = get_config_path()
    file_path_expected = os.path.join(os.getcwd(), ".coauthor.yml")
    assert file_path[0] == file_path_expected


def test_get_config_path_returns_none():
    config_path = get_config_path("whatever.yml")
    assert config_path[0] == None


def test_get_config_path_returns_file_in_home_directory():
    home_directory = os.path.expanduser("~")
    file_name = "whatever.yml"
    file_path = os.path.join(home_directory, file_name)
    with open(file_path, "w") as file:
        file.write("This is a test file created using Python.")
    config_path = get_config_path("whatever.yml", "/tmp")
    os.remove(file_path)
    assert config_path[0] == file_path


def test_get_config_returns_python():
    config = get_config()
    assert config["profile"] == "python"


def test_get_config_returns_python_with_logger():
    logger = Logger(__name__, level=logging.INFO, log_file="coauthor.log")
    logger.clean_log_file()
    config = get_config(None, logger)
    assert config["profile"] == "python"


def test_get_config_whatever_profile():
    path = os.path.join(os.path.dirname(__file__), "data", "coauthor.yml")
    config = get_config(path)
    assert config["profile"] == "whatever"


def test_get_config_not_found():
    config = get_config(config_filename="non-existing-file.yml", search_dir="/tmp")
    assert config != None


def test_get_config_not_found_with_logger():
    logger = Logger(__name__, level=logging.INFO, log_file="coauthor.log")
    logger.clean_log_file()
    config = get_config(logger=logger, config_filename="non-existing-file.yml", search_dir="/tmp")
    assert config != None


def test_config_agent_model():
    path = os.path.join(os.path.dirname(__file__), "data", "coauthor-markdown2.yml")
    config = get_config(path)
    assert config["agent"]["model"] == "llama2:latest"


def test_config_watch_directory():
    path = os.path.join(os.path.dirname(__file__), "data", "coauthor-markdown2.yml")
    path_cwd = os.getcwd()
    config = get_config(path)
    assert config["watch_directory"] == "/whatever"


def test_config_callback():
    path = os.path.join(os.path.dirname(__file__), "data", "coauthor-markdown2.yml")
    config = get_config(path)
    assert config["callback"] == "whatever_callback"


def test_config_api_url_var():
    path = os.path.join(os.path.dirname(__file__), "data", "coauthor-markdown2.yml")
    config = get_config(path)
    assert config["agent"]["api_url_var"] == "WHATEVER_URL"


def test_config_api_key_var():
    path = os.path.join(os.path.dirname(__file__), "data", "coauthor-markdown2.yml")
    config = get_config(path)
    assert config["agent"]["api_key_var"] == "WHATEVER_KEY"


def test_config_default_agent_model():
    config = get_config(config_filename="non-existing-coauthor.yml")
    assert config["agent"]["model"] == "openai/gpt-4o"


def test_config_default_watch_directory():
    config = get_config(config_filename="non-existing-coauthor.yml")
    path_cwd = os.getcwd()
    assert config["watch_directory"] == path_cwd


def test_config_default_callback():
    config = get_config(config_filename="non-existing-coauthor.yml")
    assert config["callback"] == "process_file_with_openai_agent"


def test_config_default_api_url_var():
    config = get_config(config_filename="non-existing-coauthor.yml")
    assert config["agent"]["api_url_var"] == "OPENAI_API_URL"


def test_config_default_api_key_var():
    config = get_config(config_filename="non-existing-coauthor.yml")
    assert config["agent"]["api_key_var"] == "OPENAI_API_KEY"
