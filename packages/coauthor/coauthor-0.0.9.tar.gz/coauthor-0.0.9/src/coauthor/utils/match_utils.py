import os
import re


def file_submit_to_ai(config, logger):
    """
    Return the content of the file if it requires AI processing based on path and content matching criteria.

    Parameters:
    - path (str): The path of the file to be processed.
    - task (dict): Configuration dictionary which contains optional keys 'regex_path' and
      'regex_content' for path and content validation respectively.

    Returns:
    - str: The content of the file if both path and content match the specified regex patterns in
      the task.
    - None: If the content doesn't meet the regex requirements.

    The function checks if the file path and content match the given regex patterns in the task.
    """
    path = config["current-task"]["path-modify-event"]
    path_match = file_path_match(config, logger)
    content_match = file_content_match(config, logger)
    content = None
    if path_match:
        if content_match:
            with open(path, "r", encoding="utf-8") as file1:
                content = file1.read()
    logger.debug(f"file_submit_to_ai: path_match: {path_match}, content_match: {content_match}")
    return content


def regex_content_match(content, regex, logger):
    """
    Determine if the given content matches any provided regex pattern.

    Parameters:
    - content (str): The content to be validated against the regex.
    - regex (str or list): A single regex pattern or list of regex patterns to match against the content.

    Returns:
    - bool: True if the content matches any of the regex patterns, otherwise False.

    The function checks the content against each regex pattern for a match.
    """
    if isinstance(regex, list):
        for pattern in regex:
            if isinstance(pattern, list):
                sub_patterns_all_match = True
                for sub_pattern in pattern:
                    if not re.match(sub_pattern, content, re.IGNORECASE | re.DOTALL):
                        logger.debug(f"regex_content_match: sub_patterns_all_match: False")
                        sub_patterns_all_match = False
                if sub_patterns_all_match:
                    logger.debug(f"regex_content_match: match True for pattern: {pattern}, content: {content}")
                    return True
            else:
                if re.match(pattern, content, re.IGNORECASE | re.DOTALL):  # TypeError: unhashable type: 'list'
                    logger.debug(f"regex_content_match: match: True for pattern: {pattern}, content: {content}")
                    return True
    elif isinstance(regex, str):
        if re.match(regex, content, re.IGNORECASE | re.DOTALL):
            logger.debug(f"regex_content_match: match: True for regex: {regex}, content: {content}")
            return True
    return False


def file_path_match(config, logger):
    """
    Check if the file path matches the regex pattern specified in the workflow.

    Parameters:
    - path (str): The file path to validate.
    - workflow (dict): Configuration dictionary containing the 'path_patterns' for validation.

    Returns:
    - bool: True if the path matches the regex or if no 'path_patterns' is specified, otherwise False.
    """
    workflow = config["current-workflow"]
    path = config["current-task"]["path-modify-event"]
    if "path_patterns" in workflow:
        return regex_content_match(path, workflow["path_patterns"], logger)
    return True


def file_content_match(config, logger):
    """
    Check if the file content matches the regex pattern specified in the workflow configuration.

    Parameters:
    - path (str): The path of the file whose content is to be validated.
    - workflow (dict): Configuration dictionary containing the 'content_patterns' for content validation.

    Returns:
    - bool: True if the content matches the regex, otherwise False.
    """
    workflow = config["current-workflow"]
    path = config["current-task"]["path-modify-event"]
    if not os.path.exists(path):
        logger.warning(f"file_content_match: path {path} does not exist!")
        return False

    if "content_patterns" in workflow:
        logger.debug(f"file_content_match: content_patterns: {workflow['content_patterns']}")
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        if regex_content_match(content, workflow["content_patterns"], logger):
            return True
    else:
        logger.warning(f"file_content_match: workflow has no content_patterns! So content match is false! ")
        logger.debug(f"workflow: {workflow}")
    return False


def path_new_replace(path, search, replace):
    """
    Replace a portion of the path with a new string.

    Parameters:
    - path (str): The original path string.
    - search (str): The substring to search for in the path.
    - replace (str): The string to replace the search substring with.

    Returns:
    - str: The modified path with the substitutions made.
    """
    return path.replace(search, replace)
