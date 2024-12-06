import os
from coauthor.utils.workflow_utils import get_workflows_that_watch, get_workflows_that_scan
import logging
import yaml
from coauthor.utils.logger import Logger


def get_config():
    config_path = os.path.join(os.path.dirname(__file__), "data", "coauthor-workflows.yml")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        config["current-workflow"] = config["workflows"][0]
        config["current-task"] = config["current-workflow"]["tasks"][0]
    return config


def test_get_workflows_that_watch():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    config = get_config()
    workflow = config["workflows"][0]
    workflows_that_watch = get_workflows_that_watch(config, logger)
    assert workflow == workflows_that_watch[0]


def test_get_workflows_that_scan():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    config = get_config()
    workflow = config["workflows"][0]
    workflows_that_scan = get_workflows_that_scan(config, logger)
    assert [] == workflows_that_scan
