import os
import logging
from coauthor.utils.logger import Logger
from coauthor.modules.workflow import initialize_workflows
from coauthor.utils.config import get_config
import tempfile
from tempfile import TemporaryDirectory
import yaml

# TODO enable
# def test_read_file_write_file():
#     """
#     Test the workflow that reads a file and then writes to it using specific content patterns.

#     The workflow is configured to scan files with `.md` extension, looking for content that matches
#     the pattern ".*ping.*". Upon finding such files, the "read_file" task reads the content,
#     and the "write_file" task modifies the content to append "=pong".
#     """
#     path = os.path.join(os.path.dirname(__file__), "data", "coauthor_translation2.yml")
#     with tempfile.TemporaryDirectory() as temp_dir:
#         # Create a temporary directory with a subdirectory
#         sub_dir = os.path.join(temp_dir, "subdir")
#         os.makedirs(sub_dir, exist_ok=True)

#         # Define the file path and write "ping" into it
#         file_path = os.path.join(sub_dir, "testfile.md")
#         with open(file_path, "w") as file:
#             file.write("ping")

#         # Define the configuration for the workflow
#         config = get_config(path=path)
#         workflow = config["workflows"][0]
#         workflow["scan"] = {"filesystem": {"paths": [temp_dir]}}

#         # Initialize a Logger instance for debugging
#         logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")

#         # Call the `initialize_workflows` to process the file
#         initialize_workflows(config=config, logger=logger, trigger_scan=True)

#         # Check if the content of the file was updated correctly
#         with open(file_path, "r") as file:
#             content = file.read()

#         # Assert if the content contains "ping=pong"
#         assert "ping=pong" in content
