import os
import time
import tempfile
import subprocess
import logging
from unittest.mock import patch, Mock
from coauthor.utils.logger import Logger
import pytest
from coauthor.modules.file_watcher import watch_directory, add_watch_recursive, watch
from inotify_simple import flags
import sys
import yaml
import threading


def get_config(config_file="coauthor_task_pong.yml"):
    config_path = os.path.join(os.path.dirname(__file__), "data", config_file)
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        config["current-workflow"] = config["workflows"][0]
        config["current-task"] = config["current-workflow"]["tasks"][0]
    return config


class TestWatchDirectory:
    @pytest.fixture
    def setup_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    def test_watch_directory(self, setup_directory):
        temp_dir = setup_directory
        logger = Logger("test_watch_directory", level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
        config = get_config()
        config["current-workflow"] = config["workflows"][0]
        config["current-workflow"]["watch"] = {"filesystem": {"paths": [temp_dir]}}
        config["current-task"] = config["current-workflow"]["tasks"][0]
        file_path = os.path.join(temp_dir, "test_file.md")
        config["current-task"]["path-modify-event"] = file_path
        watch_directories = [f"{temp_dir}"]
        with open(file_path, "w") as f:
            f.write("whatever")
        x = threading.Thread(target=watch_directory, args=(config, logger), daemon=True)
        x.start()

        time.sleep(3)

        with open(file_path, "w") as f:
            f.write("@ai-test: ping")
        file_contents = pytest.helpers.wait_file_content(file_path, "pong", retries=10, delay=1)
        assert file_contents == "pong"

        with open(os.path.join(temp_dir, "stop"), "w") as f:
            f.write("stop")

    def test_watch_and_multiple_files_in_subdir(self, setup_directory):
        temp_dir = setup_directory
        logger = Logger("test_watch_directory", level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
        config = get_config()
        config["current-workflow"] = config["workflows"][0]
        config["current-workflow"]["watch"] = {"filesystem": {"paths": [temp_dir]}}
        config["current-task"] = config["current-workflow"]["tasks"][0]
        file_path_1 = os.path.join(temp_dir, "test_file.md")
        with open(file_path_1, "w") as f:
            f.write("whatever")
        new_dir = os.path.join(temp_dir, "new_directory")
        os.makedirs(new_dir)
        file_path_2 = os.path.join(new_dir, "test_file.md")
        with open(file_path_2, "w") as f:
            f.write("whatever")

        # watch_directory(config, logger)  # TODO keep disabled
        x = threading.Thread(target=watch_directory, args=(config, logger), daemon=True)
        x.start()
        assert x.is_alive(), "The thread for watching the directory did not start successfully"
        time.sleep(3)

        with open(file_path_1, "w") as f:
            f.write("@ai-test: ping")
        file_contents = pytest.helpers.wait_file_content(file_path_1, "pong", retries=10, delay=1)
        assert file_contents == "pong"

        with open(file_path_2, "w") as f:
            f.write("@ai-test: ping")
        file_contents = pytest.helpers.wait_file_content(file_path_2, "pong", retries=10, delay=1)
        assert file_contents == "pong"

        with open(os.path.join(temp_dir, "stop"), "w") as f:
            f.write("stop")

        x.join()

    def test_watch_and_multiple_regex_callbacks(self, setup_directory):
        temp_dir = setup_directory
        logger = Logger("test_watch_directory", level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
        config = get_config("coauthor-regex-replace.yml")
        config["current-workflow"] = config["workflows"][0]
        config["current-workflow"]["watch"] = {"filesystem": {"paths": [temp_dir]}}
        config["current-task"] = config["current-workflow"]["tasks"][0]

        # watch_directory(config, logger)  # TODO keep disabled
        x = threading.Thread(target=watch_directory, args=(config, logger), daemon=True)
        x.start()
        assert x.is_alive(), "The thread for watching the directory did not start successfully"

        new_dir = os.path.join(temp_dir, "new_directory")
        new_dir_2 = os.path.join(new_dir, "new_directory")
        new_file_path = os.path.join(new_dir, "new_test_file.txt")
        new_file_path2 = os.path.join(new_dir_2, "new_test_file.txt")

        os.makedirs(new_dir)
        os.makedirs(new_dir_2)

        assert True

        time.sleep(3)
        with open(new_file_path, "w") as f:
            f.write("a -> b")
        file_contents = pytest.helpers.wait_file_content(new_file_path, "a → b", retries=10, delay=1)
        assert file_contents == "a → b"

        with open(new_file_path2, "w") as f:
            f.write("a <- b")
        file_contents = pytest.helpers.wait_file_content(new_file_path2, "a ← b", retries=10, delay=1)
        assert file_contents == "a ← b"

        # Stop watch directory using stop file
        with open(os.path.join(temp_dir, "stop"), "w") as f:
            f.write("stop")
        x.join()


class TestWatchUtils:
    @pytest.fixture
    def mock_inotify(self):
        with patch("coauthor.modules.file_watcher.INotify") as MockINotify:
            yield MockINotify()

    @pytest.fixture
    def setup_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    def test_add_watch_recursive(self, setup_directory, mock_inotify):
        temp_dir = setup_directory
        wd_to_path = add_watch_recursive(mock_inotify, temp_dir)

        mock_inotify.add_watch.assert_any_call(temp_dir, flags.CREATE | flags.MODIFY)

        for root, dirs, _ in os.walk(temp_dir):
            for subdir in dirs:
                subdir_path = os.path.join(root, subdir)
                mock_inotify.add_watch.assert_any_call(subdir_path, flags.CREATE | flags.MODIFY)

        expected_wd_to_path = {mock_inotify.add_watch.return_value: path for path in wd_to_path.values()}
        assert wd_to_path == expected_wd_to_path
