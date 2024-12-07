from typing import Dict, Any, Optional

from codemie_tools.base.base_toolkit import BaseToolkit
from codemie_tools.base.models import ToolKit, ToolSet, Tool
from codemie_tools.pandas.csv_tool import CSVTool
from codemie_tools.pandas.tool_vars import CSV_TOOL


class PandasToolkit(BaseToolkit):
    csv_content: Optional[Any] = None

    @classmethod
    def get_tools_ui_info(cls, *args, **kwargs):
        return ToolKit(
            toolkit=ToolSet.PANDAS,
            tools=[
                Tool.from_metadata(CSV_TOOL),
            ]
        ).model_dump()

    def get_tools(self):
        return [CSVTool(csv_content=self.csv_content)]

    @classmethod
    def get_toolkit(cls, configs: Dict[str, Any]):
        csv_content = configs.get("csv_content", None)
        return cls(csv_content=csv_content)
