from typing import Any, Dict, List, Optional, Type, Union

from bs4 import BeautifulSoup
from pydantic import BaseModel


class Lox:
    linkedin_email: str
    linkedin_password: str
    notion_api_key: str
    notion_database_id: str
    notion_schema: Dict[str, Any]
    notion_headers: Dict[str, str]

    def __init__(
        self,
        linkedin_email: Optional[str] = None,
        linkedin_password: Optional[str] = None,
        notion_api_key: Optional[str] = None,
        notion_database_id: Optional[str] = None,
    ) -> None: ...

    def get_post_content(self, url: str) -> Optional[str]: ...
    def get_notion_fields(self) -> List[str]: ...
    def write_to_notion(self, data: Dict[str, Any]) -> bool: ...
    def read_from_notion(self) -> Dict[str, Any]: ...


def build_pydantic_model(fields: List[str]) -> Type[BaseModel]: ...


def extract_json_fields(
    content: Union[str, BeautifulSoup], PydanticModel: Type[BaseModel], model: str = ...
) -> Dict[str, Any]: ...
