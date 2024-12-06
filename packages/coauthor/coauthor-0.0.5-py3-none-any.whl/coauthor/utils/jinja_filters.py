import logging
from coauthor.utils.logger import Logger
import os


class TaskNotFoundError(Exception):
    """Exception raised when a task with the specified ID is not found."""

    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(f"Task with ID {self.task_id} not found.")


class AttributeNotFoundError(Exception):
    """Exception raised when a specified attribute is not found in a task."""

    def __init__(self, attribute):
        self.attribute = attribute
        super().__init__(f"Attribute '{self.attribute}' not found in task.")


def select_task(config, task_id):
    """
    Select and return a task from a list of tasks based on its id.

    :param tasks: a list of task dictionaries
    :param id: the id of the task to find
    :return: The task dictionary with the matching id
    :raises TaskNotFoundError: If no task with the given id is found
    """
    workflow = config["current-workflow"]
    for task in workflow["tasks"]:
        if task.get("id") == task_id:
            return task
    raise TaskNotFoundError(task_id)


def get_task_attribute(config, id, attribute):
    """
    Get a specific attribute from a task identified by id.

    :param tasks: a list of task dictionaries
    :param id: the id of the task from which to get the attribute
    :param attribute: the attribute to retrieve from the task
    :return: The value of the specified attribute in the task
    :raises TaskNotFoundError: If no task with the given id is found
    :raises AttributeNotFoundError: If the attribute does not exist in the task
    """
    task = select_task(config, id)
    if attribute in task:
        return task[attribute]
    else:
        raise AttributeNotFoundError(attribute)
