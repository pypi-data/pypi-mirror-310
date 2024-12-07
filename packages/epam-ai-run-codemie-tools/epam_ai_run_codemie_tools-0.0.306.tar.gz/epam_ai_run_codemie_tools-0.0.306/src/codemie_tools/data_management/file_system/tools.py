import logging
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Type, Optional, Any

from langchain_community.tools.file_management.utils import FileValidationError, INVALID_PATH_TEMPLATE
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import ToolException
from pydantic import BaseModel, Field

from codemie_tools.base.codemie_tool import CodeMieTool
from codemie_tools.code.coder.diff_update_coder import update_content_by_task
from codemie_tools.data_management.file_system.tools_vars import (
    READ_FILE_TOOL, LIST_DIRECTORY_TOOL, WRITE_FILE_TOOL, COMMAND_LINE_TOOL, DIFF_UPDATE_FILE_TOOL
)
from codemie_tools.data_management.file_system.utils import get_relative_path, create_folders

logger = logging.getLogger(__name__)

class ReadFileInput(BaseModel):
    file_path: str = Field(..., description="File path to read from file system")


class ReadFileTool(CodeMieTool):
    name: str = READ_FILE_TOOL.name
    args_schema: Type[BaseModel] = ReadFileInput
    description: str = READ_FILE_TOOL.description
    root_dir: Optional[str] = "."

    def execute(self, file_path: str, raise_error=False, *args, **kwargs) -> str:
        try:
            read_path = get_relative_path(self.root_dir, file_path)
        except FileValidationError:
            return INVALID_PATH_TEMPLATE.format(arg_name="file_path", value=file_path)
        if not read_path.exists():
            if raise_error:
                raise FileNotFoundError(f"Error: no such file or directory: {file_path}")
            else:
                return f"Error: no such file or directory: {file_path}"
        try:
            with read_path.open("r", encoding="utf-8") as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error: {e}"


class DirectoryListingInput(BaseModel):
    """Input for ListDirectoryTool."""

    dir_path: str = Field(default=".", description="Subdirectory to list.")


class ListDirectoryTool(CodeMieTool):
    """Tool that lists files and directories in a specified folder."""

    name: str = LIST_DIRECTORY_TOOL.name
    args_schema: Type[BaseModel] = DirectoryListingInput
    description: str = LIST_DIRECTORY_TOOL.description
    root_dir: Optional[str] = "."

    def execute(self, dir_path: str = ".", *args, **kwargs) -> str:
        try:
            dir_path_ = get_relative_path(self.root_dir, dir_path)
        except FileValidationError:
            return INVALID_PATH_TEMPLATE.format(arg_name="dir_path", value=dir_path)
        try:
            entries = os.listdir(dir_path_)
            if entries:
                return "\n".join(entries)
            else:
                return f"No files found in directory {dir_path}"
        except Exception as e:
            return f"Error: {e}"


class WriteFileInput(BaseModel):
    file_path: str = Field(..., description="File path to write to file system")
    text: str = Field(..., description="Content or text to write to file.")


class WriteFileTool(CodeMieTool):
    name: str = WRITE_FILE_TOOL.name
    args_schema: Type[BaseModel] = WriteFileInput
    description: str = WRITE_FILE_TOOL.description
    root_dir: Optional[str] = "."

    def execute(self, file_path: str, text: str) -> str:
        try:
            write_path = get_relative_path(self.root_dir, file_path)
        except FileValidationError:
            return INVALID_PATH_TEMPLATE.format(arg_name="file_path", value=file_path)
        try:
            create_folders(write_path)
            write_path.parent.mkdir(exist_ok=True, parents=False)
            mode = "w"
            with write_path.open(mode, encoding="utf-8") as f:
                f.write(text)

            return f"File written successfully to {file_path}"
        except Exception as e:
            return f"Error: {e}"


class CommandLineInput(BaseModel):
    command: str = Field(
        description="Command to execute in the CLI."
    )


class DiffUpdateFileToolInput(BaseModel):
    task_details: str = Field(description="""String. Specify detailed task description for file which must be updated 
    or provide detailed generated reference what should be done""")
    file_path: str = Field(..., description="File path of the file that should be updated by task details")
    should_create: bool = Field(default=False, description="Whether the file should be created if it does not exist.")


class CommandLineTool(CodeMieTool):
    name: str = COMMAND_LINE_TOOL.name
    description: str = COMMAND_LINE_TOOL.description
    args_schema: Type[BaseModel] = CommandLineInput
    root_dir: Optional[str] = "."
    timeout: int = 60

    def __init__(self, root_dir: str = "."):
        super().__init__()
        self.root_dir = root_dir

    def execute(self, command: str, *args, **kwargs) -> Any:
        CommandLineTool.sanitize_command(command)
        work_dir = Path(self.root_dir)
        work_dir.mkdir(exist_ok=True)

        command_start_time = int(round(time.time() * 1000))

        result = subprocess.run(
            command, cwd=work_dir, shell=True, text=True, capture_output=True, timeout=float(self.timeout)
        )

        # Return a dictionary with the desired information
        return result.stdout, result.stderr, result.returncode, command_start_time

    @staticmethod
    def sanitize_command(command: str) -> None:
        """
        Sanitize the code block to prevent dangerous commands.
        This approach acknowledges that while Docker or similar
        containerization/sandboxing technologies provide a robust layer of security,
        not all users may have Docker installed or may choose not to use it.
        Therefore, having a baseline level of protection helps mitigate risks for users who,
        either out of choice or necessity, run code outside of a sandboxed environment.
        """
        dangerous_patterns = [
            (r"\brm\s+-rf\b", "Use of 'rm -rf' command is not allowed."),
            (r"\bmv\b.*?\s+/dev/null", "Moving files to /dev/null is not allowed."),
            (r"\bdd\b", "Use of 'dd' command is not allowed."),
            (r">\s*/dev/sd[a-z][1-9]?", "Overwriting disk blocks directly is not allowed."),
            (r":\(\)\{\s*:\|\:&\s*\};:", "Fork bombs are not allowed."),
        ]
        for pattern, message in dangerous_patterns:
            if re.search(pattern, command):
                logger.error(f"Potentially dangerous command detected: {message}")
                raise ToolException(f"Potentially dangerous command detected: {message}")


class DiffUpdateFileTool(CodeMieTool):
    name: str = DIFF_UPDATE_FILE_TOOL.name
    args_schema: Type[BaseModel] = DiffUpdateFileToolInput
    description: str = DIFF_UPDATE_FILE_TOOL.description
    root_dir: Optional[str] = "."
    llm_model: Optional[BaseChatModel] = Field(exclude=True)
    handle_validation_error: bool = True

    def execute(self, file_path: str, task_details: str, should_create: bool = False) -> str:
        read_path = get_relative_path(self.root_dir, file_path)
        if not read_path.exists():
            if should_create:
                create_folders(read_path)
                read_path.touch()
            else:
                return f"Error: no such file or directory: {file_path}"
        with read_path.open("r", encoding="utf-8") as f:
            content = f.read()

        new_content, edits = update_content_by_task(content, task_details, self.llm_model)

        with read_path.open("w", encoding="utf-8") as f:
            f.write(new_content)

        return f"Changes have been successfully applied to the file {file_path}:\n{edits}"
