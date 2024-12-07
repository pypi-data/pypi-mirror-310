import logging

from atlassian import Jira

from langchain_core.tools import ToolException

logger = logging.getLogger(__name__)


def validate_jira_creds(jira: Jira):
    if jira.url is None or jira.url == "":
        logger.error("Jira URL is required. Seems there no Jira credentials provided.")
        raise ToolException("Jira URL is required. Seems there no Jira credentials provided.")
