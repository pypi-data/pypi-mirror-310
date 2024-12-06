import os
import time
from coauthor.modules.ai import process_file_with_openai_agent

from coauthor.utils.workflow_utils import get_workflows_that_scan
from coauthor.modules.file_processor import regex_replace_in_file, pong
from coauthor.modules.workflow_tasks import write_file, read_file

task_type_functions = {
    "process_file_with_openai_agent": process_file_with_openai_agent,
    "regex_replace_in_file": regex_replace_in_file,
    "pong": pong,
    "write_file": write_file,
    "read_file": read_file,
}


def scan(config, logger):
    workflows_that_scan = get_workflows_that_scan(config, logger)
    logger.debug(f"workflows_that_scan: {workflows_that_scan}")
    for workflow in workflows_that_scan:
        scan_directories = workflow["scan"]["filesystem"]["paths"]
        logger.info(f"Workflow {workflow['name']}: scan directories {', '.join(scan_directories)}")

        wd_to_path = {}
        for directory in scan_directories:
            for root, _, files in os.walk(directory):
                for filename in files:
                    path = os.path.join(root, filename)
                    handle_workflow_scan_file(path, workflow, config, logger)


def handle_workflow_scan_file(path, workflow, config, logger):
    logger.info(f"Processing file {path}")
    for task in workflow["tasks"]:
        logger.debug(f"task: {task}")
        if task["type"] in task_type_functions:
            logger.debug(f"Workflow: {workflow['name']}, Task: {task['id']} → {path}")
            if "path-modify-event" not in task:
                task["path-modify-event"] = path
            config["current-task"] = task
            config["current-workflow"] = workflow
            task_type_functions[task["type"]](config, logger)
        else:
            raise ValueError(f'Unsupported task_type: {task["type"]}')
