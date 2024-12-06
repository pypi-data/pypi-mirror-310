import os
import yaml
import logging
from coauthor.utils.logger import Logger
from coauthor.utils.match_utils import (
    regex_content_match,
    file_submit_to_ai,
    file_content_match,
    path_new_replace,
)


def get_config():
    config_path = os.path.join(os.path.dirname(__file__), "data", "coauthor_test_match_utils.yml")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        config["current-workflow"] = config["workflows"][0]
        config["current-task"] = config["current-workflow"]["tasks"][0]
    return config


def test_file_submit_to_ai():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    config = get_config()
    path = os.path.join(os.path.dirname(__file__), "data", "whatever.md")
    task = config["current-task"]
    task["path-modify-event"] = path
    with open(path) as f:
        content_expected = f.read()
    content = file_submit_to_ai(config, logger)
    assert content == content_expected


def test_file_submit_to_ai_wrong_extension():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    config = get_config()
    task = config["current-task"]
    path = os.path.join(os.path.dirname(__file__), "data", "whatever.txt")
    task["path-modify-event"] = path
    content = file_submit_to_ai(config, logger)
    assert content is None


def test_file_submit_to_ai_no_regex():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    config = get_config()
    task = config["current-task"]
    task["path-modify-event"] = os.path.join(os.path.dirname(__file__), "data", "whatever.md")
    del config["current-workflow"]["content_patterns"]
    content = file_submit_to_ai(config, logger)
    assert content is None


def test_file_submit_to_ai_no_instruction_in_content():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    config = get_config()
    task = config["current-task"]
    task["path-modify-event"] = os.path.join(os.path.dirname(__file__), "data", "whatever_without_instruction.md")
    content = file_submit_to_ai(config, logger)
    assert content is None


def test_path_markdown():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    assert regex_content_match("whatever.md", ".*\\.md$", logger)


def test_path_markdown_path_subdir():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    assert regex_content_match("/a/b/c/whatever.md", ".*\\.md$", logger)


def test_path_markdown_no_extension():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    assert not regex_content_match("/a/b/c/whatever", ".*\\.md$", logger)


def test_path_markdown_wrong_extension():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    assert not regex_content_match("/a/b/c/whatever.txt", ".*\\.md$", logger)


def test_content_ai_instruction():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    content = """
whatever
(aiaiai: do whatever)
"""
    assert regex_content_match(content, ".*\\(aiaiai:.*?\\).*", logger)


def test_content_ai_instruction_multiline():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    content = """
whatever
(aiaiai: do whatever
do whatever
)
"""
    assert regex_content_match(content, ".*\\(aiaiai:.*?\\).*", logger)


def test_content_ai_instruction_multiline_2():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    content = """
whatever (aiaiai: do whatever
do whatever
do whatever do whatever)
"""
    assert regex_content_match(content, ".*\\(aiaiai:.*?\\).*", logger)


def test_regex_content_match_with_list():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    content = """
whatever (aiaiai: do whatever
do whatever
do whatever do whatever)
"""
    regex_list = [".*\\(aiaiai:.*?\\).*", "whatever"]

    # The function should return True as one of the patterns matches the content
    assert regex_content_match(content, regex_list, logger)

    # Testing with a list of patterns that don't match
    regex_list_no_match = [".*\\(ai-ai:.*?\\).*", "whatever"]

    # The function should return False as none of these patterns match the content
    assert not regex_content_match(content, regex_list_no_match, logger)


def test_file_content_match_file_does_not_exist():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    config = get_config()
    task = config["current-task"]
    task["path-modify-event"] = "/tmp/a/file/that/doesn't/exist"
    assert not file_content_match(config, logger)


def test_path_new_replace():
    path = "/home/user/content/en/docs/guidelines/coding/tags/example.md"
    path_expected = "/home/user/content/nl/docs/guidelines/coding/tags/example.md"
    search = "content/en/docs"
    replace = "content/nl/docs"
    path_replaced = path_new_replace(path, search, replace)
    assert path_replaced == path_expected


def test_regex_content_match_with_sub_patterns():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    content = """
whatever (aiaiai: do this and that)
"""
    regex_list = [[".*\\(aiaiai:.*and.*\\).*", ".*whatever.*"], "another_pattern"]
    assert regex_content_match(content, regex_list, logger)

    regex_list_no_match = [[".*\\(aiaiai:.*or.*\\).*", "whatever"], "another_pattern"]
    assert not regex_content_match(content, regex_list_no_match, logger)


def test_regex_content_match_with_string():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    content = "sample content"
    assert not regex_content_match(content, "another_sample", logger)
    assert regex_content_match(content, "sample", logger)
    assert not regex_content_match(content, None, logger)
