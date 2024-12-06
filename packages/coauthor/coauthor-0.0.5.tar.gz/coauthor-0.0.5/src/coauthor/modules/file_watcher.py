import os
import time
from inotify_simple import INotify, flags

from coauthor.utils.workflow_utils import (
    get_workflows_that_watch,
    get_workflows_that_scan,
    get_all_scan_directories_from_workflows,
    get_all_watch_directories_from_workflows,
)
from coauthor.utils.match_utils import file_path_match, file_content_match
from coauthor.modules.ai import process_file_with_openai_agent
from coauthor.modules.file_processor import regex_replace_in_file, pong
from coauthor.modules.workflow_tasks import write_file, read_file

task_type_functions = {
    "process_file_with_openai_agent": process_file_with_openai_agent,
    "regex_replace_in_file": regex_replace_in_file,
    "pong": pong,
    "write_file": write_file,
    "read_file": read_file,
}

# Initialize a dictionary to store the last modification time of each file based
# on workflow and task
last_modification_times = {}


def add_watch_recursive(inotify, directory):
    """Recursively add watches on all subdirectories,
    ignoring certain directories."""
    wd_to_path = {}
    for root, dirs, files in os.walk(directory):
        # Ignore specific directories like __pycache__  # TODO .obsidian directory
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        wd = inotify.add_watch(root, flags.CREATE | flags.MODIFY)
        wd_to_path[wd] = root
    return wd_to_path


def watch(config, logger):
    watch_directory(config, logger)


def handle_inotify_event(event, wd_to_path, inotify, config, logger):
    """Handle inotify events by accurately determining the file changed.

    For MODIFY events, due to some editors' behavior of replacing files rather than directly modifying them,
    this function identifies the most recently updated file in the event's directory as the file affected by the event.
    """
    directory = wd_to_path.get(event.wd, "")
    logger.debug(
        f"Inotify Event: directory={directory}, event_mask={event.mask}, flags.from_mask={flags.from_mask(event.mask)}"
    )

    # Find the most recently modified file in the directory, ignoring hidden files
    def get_recently_modified_file(file_path_inotify, dir_path, logger):
        all_files = [
            os.path.join(dir_path, f)
            for f in os.listdir(dir_path)
            if os.path.isfile(os.path.join(dir_path, f)) and not f.startswith(".")
        ]
        logger.debug(f"all_files: {', '.join(all_files)}")
        if file_path_inotify in all_files:
            return file_path_inotify
        return max(all_files, key=os.path.getmtime) if all_files else None

    file_path_inotify = os.path.join(directory, event.name)
    file_path = get_recently_modified_file(file_path_inotify, directory, logger)

    # Check if it is a directory and add watch if new directory is created
    if flags.CREATE in flags.from_mask(event.mask) and os.path.isdir(file_path_inotify):
        logger.info(f"Watching new directory: {file_path_inotify}")
        wd = inotify.add_watch(file_path_inotify, flags.CREATE | flags.MODIFY | flags.CLOSE_WRITE)
        wd_to_path[wd] = file_path_inotify

    if file_path_inotify != file_path:
        logger.warning(f"file_path_inotify: {file_path_inotify} is not equal to file_path: {file_path}")
        logger.debug(" this can occur depending on how editors write changes to files")
        logger.debug(" For example Gedit uses a temporary file .goutputstream-G1SHX2")
        file_path_selected = file_path
        time.sleep(2)  # allow Gedit some time to finish updating file
    else:
        file_path_selected = file_path_inotify

    ignore_extensions = config.get("watch-ignore-file-extensions", [])
    if flags.MODIFY in flags.from_mask(event.mask) and file_path_selected:
        file_extension = os.path.splitext(file_path_selected)[1]
        if file_extension not in ignore_extensions:
            logger.info(f"MODIFY event: file_path_inotify: {file_path_selected}")
            handle_workflow_file_modify_event(file_path_selected, config, logger)

    # Stop the process if `stop` file is created
    if os.path.basename(file_path_selected) == "stop":
        logger.info("Stop file found!")
        os.remove(file_path_selected)
        return True

    return False


def watch_directory(config, logger):
    watch_directories = get_all_watch_directories_from_workflows(config, logger)
    inotify = INotify()

    logger.info(f"Watching directories recursively: {', '.join(watch_directories)}")

    wd_to_path = {}
    for directory in watch_directories:
        wd_to_path.update(add_watch_recursive(inotify, directory))

    try:
        while True:
            for event in inotify.read():
                if handle_inotify_event(event, wd_to_path, inotify, config, logger):
                    return
    except KeyboardInterrupt:
        print("Stopping directory watch")
    finally:
        for wd in wd_to_path.keys():
            inotify.rm_watch(wd)


def handle_workflow_file_modify_event(path, config, logger):
    workflows_that_watch = get_workflows_that_watch(config, logger)
    logger.debug(f"get_workflows_that_watch: workflows_that_watch: {workflows_that_watch}")
    for workflow in workflows_that_watch:
        config["current-workflow"] = workflow
        logger.debug(f"workflow: {workflow}")
        for task in workflow["tasks"]:
            config["current-task"] = task
            task["path-modify-event"] = path
            path_match = file_path_match(config, logger)
            if "content_patterns" in workflow:
                content_match = file_content_match(config, logger)
                logger.debug(f'Workflow has no "content_patterns", so "content_match" is True')
            else:
                content_match = True
            if not path_match or not content_match:
                logger.debug(f"No path or content match on {path}")
                continue
            logger.info(f"Path and content match on {path}")
            if task["type"] in task_type_functions:
                logger.info(f"Workflow: {workflow['name']}, Task: {task['id']} → {path}")
                if not ignore_rapid_modify_event(path, config, logger):
                    task_type_functions[task["type"]](config, logger)
            else:
                raise ValueError(f'Unsupported task_type: {task["type"]}')


# Some tools / IDE depending on configuraton  / extensions / plugins might cause
# multiple modify events. To distinquishd from technical save from user save
# we can set a time limit and ignore the same modify event
def ignore_rapid_modify_event(path, config, logger):
    current_time = time.time()
    workflow = config["current-workflow"]
    task = config["current-task"]
    # Determine unique key based on file path, workflow and task id
    key = (path, workflow["name"], task["id"])
    last_time = last_modification_times.get(key, 0)

    modify_event_limit = 3
    if "modify_event_limit" in task:
        modify_event_limit = task["modify_event_limit"]

    # If the time since the last modification event is less than
    # modify_event_limit, ignore this event
    if current_time - last_time < modify_event_limit:
        logger.info(f"  Ignoring rapid MODIFY event for (modify_event_limit: {modify_event_limit}).")
        return True
    last_modification_times[key] = current_time
    logger.debug(f"  NOT ignoring rapid MODIFY event for (modify_event_limit: {modify_event_limit}).")
    return False
