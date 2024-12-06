# from coauthor.modules.file_watcher import watch
# from coauthor.modules.file_scanner import scan
# from coauthor.modules.ai import process_file_with_openai_agent
# from coauthor.modules.file_processor import pong, regex_replace_in_file

# from coauthor.modules.workflow_tasks import read_file, write_file
from coauthor.modules.file_scanner import scan
from coauthor.modules.file_watcher import watch
from coauthor.utils.workflow_utils import (
    get_all_scan_directories_from_workflows,
    get_all_watch_directories_from_workflows,
)


def initialize_workflows(config, logger, trigger_scan=False):
    if not "workflows" in config:
        logger.warning("No workflows in config, nothing to do")
        return
    args = config.get("args", None)
    if (args and args.scan) or trigger_scan:
        logger.info("Scan mode enabled with --scan")
        scan_directories = get_all_scan_directories_from_workflows(config, logger)
        logger.info(f"scan_directories: {', '.join(scan_directories)}")
        if len(scan_directories) > 0:
            scan(config, logger)
        else:
            logger.debug(f"No scan directories!")
    if args and args.watch:
        watch_directories = get_all_watch_directories_from_workflows(config, logger)
        logger.info("Watch mode enabled with --watch")
        if len(watch_directories) > 0:
            watch(config, logger)
