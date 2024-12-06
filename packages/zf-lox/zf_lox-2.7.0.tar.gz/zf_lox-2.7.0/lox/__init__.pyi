from typing import Any, Dict, Type, Union
from bs4 import BeautifulSoup
from pydantic import BaseModel
from .lox import Lox
from .utils import build_pydantic_model

def extract_json_fields(
    content: Union[str, BeautifulSoup],
    PydanticModel: Type[BaseModel],
    model: str = ...
) -> Dict[str, Any]: ... 