import yaml
import os


def read_config(file_path, logger=None):
    if logger:
        logger.info(f"Reading configuration from {file_path}")
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def get_config_path(config_filename=".coauthor.yml", search_dir=os.getcwd()):
    # Search current directory and traverse upwards to all parent directories
    traversed_paths = []
    while True:
        potential_path = os.path.join(search_dir, config_filename)
        if os.path.exists(potential_path):
            return potential_path, traversed_paths
        # Append to traversed paths for logging purposes
        traversed_paths.append(search_dir)
        # Move up one directory
        parent_dir = os.path.dirname(search_dir)
        if parent_dir == search_dir:  # If reached the root directory
            break
        search_dir = parent_dir

    # Check in user's home directory
    home_dir = os.path.expanduser("~")
    home_path = os.path.join(home_dir, config_filename)
    if os.path.exists(home_path):
        traversed_paths.append(home_dir)
        return home_path, traversed_paths

    # If no config file is found, return None and the paths checked
    return None, traversed_paths


def get_config(path=None, logger=None, config_filename=".coauthor.yml", search_dir=os.getcwd(), args=None):
    config = {}
    config_path = None
    if args and "config_path" in args:
        config_path = args.config_path
    if not config_path:
        if path:
            # config_path = read_config(path, logger)
            config_path = path
        else:
            config_path, searched_paths = get_config_path(config_filename, search_dir)
            if not config_path:
                if logger:
                    logger.warning(f"Configuration file not found. Searched directories: {', '.join(searched_paths)}")
    if config_path:
        config = read_config(config_path, logger)
    if "watch_directory" not in config:
        config["watch_directory"] = os.getcwd()
    if "callback" not in config and "callbacks" not in config:
        config["callback"] = "process_file_with_openai_agent"
    if "agent" not in config or config["agent"] is None:
        config["agent"] = {}
    if not "api_key_var" in config["agent"]:
        config["agent"]["api_key_var"] = "OPENAI_API_KEY"
    if not "api_url_var" in config["agent"]:
        config["agent"]["api_url_var"] = "OPENAI_API_URL"
    if not "model" in config["agent"]:
        config["agent"]["model"] = "openai/gpt-4o"
    return config


def get_jinja_config(config):
    if "jinja" in config:
        return config["jinja"]
    config_jinja = {"search_path": ".coauthor/templates"}
    return config_jinja
