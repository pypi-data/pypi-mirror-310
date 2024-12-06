import re
import time
from coauthor.utils.match_utils import file_path_match


def pong(config, logger):
    path = config["current-task"]["path-modify-event"]
    logger.info("Running pong file processor " + path)
    time.sleep(3)
    with open(path, "r") as file:
        file_contents = file.read()
    if file_contents != "pong":
        logger.info(f'Updating {path} to "pong"')
        with open(path, "w") as f:
            f.write("pong")


def regex_replace_in_file(config, logger):
    task = config["current-task"]
    path = task["path-modify-event"]
    path_match = file_path_match(config, logger)
    if not path_match:
        logger.debug(f"regex_replace_in_file: no path match for {path}")
        return False
    patterns = task["patterns"]

    # Open the file and read the content
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    original_content = content

    # Apply each regex pattern and handle internal matches/replacement if needed
    for pattern_set in patterns:
        logger.debug(f"regex_replace_in_file: {path}, patterns: {pattern_set}")
        pattern = pattern_set["regex"]

        # Check for internal modifications based on run-time conditions
        internal_regex = pattern_set.get("internal_regex")
        internal_replace = pattern_set.get("internal_replace")
        if internal_regex and internal_replace:
            content = re.sub(
                pattern,
                lambda match: re.sub(
                    internal_regex,
                    internal_replace,
                    match.group(0),
                ),
                content,
            )
        else:
            replace = pattern_set["replace"]
            content = re.sub(pattern, replace, content)

    if content == original_content:
        logger.debug("regex_replace_in_file: no content was changed")
        return False

    logger.info(f"Regex patterns changed file {path}, patterns: {patterns}")
    task["content"] = content
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
        time.sleep(3)
    return True
