from typing import List, Optional, Any, Dict

from atlassian import Jira, Confluence
from pydantic import BaseModel, model_validator

from codemie_tools.base.base_toolkit import BaseToolkit
from codemie_tools.base.models import ToolKit, ToolSet, Tool
from codemie_tools.project_management.confluence.generic_confluence_tool import GenericConfluenceTool
from codemie_tools.project_management.confluence.tools_vars import GENERIC_CONFLUENCE_TOOL
from codemie_tools.project_management.jira.generic_tool import GenericJiraIssueTool
from codemie_tools.project_management.jira.tools_vars import GENERIC_JIRA_TOOL


class JiraConfig(BaseModel):
    url: str
    username: Optional[str] = None
    token: str
    cloud: Optional[bool] = False

    @classmethod
    @model_validator(mode='before')
    def validate_config(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ['url', 'token']
        for field in required_fields:
            if field not in values or not values[field]:
                raise ValueError(f"{field} is a required field and must be provided.")
        return values


class ConfluenceConfig(BaseModel):
    url: str
    username: Optional[str] = None
    token: str
    cloud: Optional[bool] = False

    @classmethod
    @model_validator(mode='before')
    def validate_config(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ['url', 'token']
        for field in required_fields:
            if field not in values or not values[field]:
                raise ValueError(f"{field} is a required field and must be provided.")
        return values


class ProjectManagementToolkitUI(ToolKit):
    toolkit: ToolSet = ToolSet.PROJECT_MANAGEMENT
    tools: List[Tool] = [
        Tool.from_metadata(GENERIC_JIRA_TOOL, settings_config=True),
        Tool.from_metadata(GENERIC_CONFLUENCE_TOOL, settings_config=True)
    ]
    label: str = ToolSet.PROJECT_MANAGEMENT.value


class ProjectManagementToolkit(BaseToolkit):
    jira_config: Optional[JiraConfig] = None
    confluence_config: Optional[ConfluenceConfig] = None

    @classmethod
    def get_tools_ui_info(cls):
        return ProjectManagementToolkitUI().model_dump()

    def get_tools(self) -> list:
        tools = []
        if self.jira_config:
            if self.jira_config.cloud:
                jira = Jira(
                    url=self.jira_config.url,
                    username=self.jira_config.username,
                    password=self.jira_config.token,
                    cloud=True,
                )
            else:
                jira = Jira(
                    url=self.jira_config.url,
                    token=self.jira_config.token,
                    cloud=False,
                )
            tools.append(GenericJiraIssueTool(jira=jira))
        if self.confluence_config:
            if self.confluence_config.cloud:
                confluence = Confluence(
                    url=self.confluence_config.url,
                    username=self.confluence_config.username,
                    password=self.confluence_config.token,
                    cloud=True,
                )
            else:
                confluence = Confluence(
                    url=self.confluence_config.url,
                    token=self.confluence_config.token,
                    cloud=False,
                )
            tools.append(GenericConfluenceTool(confluence=confluence))
        return tools

    @classmethod
    def get_toolkit(cls, configs: Dict[str, Any]):
        jira_config = JiraConfig(**configs["jira"]) if "jira" in configs else None
        confluence_config = ConfluenceConfig(**configs["confluence"]) if "confluence" in configs else None
        return cls(jira_config=jira_config,
                   confluence_config=confluence_config)
