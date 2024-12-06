from .lox import Lox
from .utils import build_pydantic_model
from typing import Any, Dict, Type, Union
from bs4 import BeautifulSoup
from pydantic import BaseModel
from perse import extract_json_fields as _extract_json_fields

def extract_json_fields(
    content: Union[str, BeautifulSoup],
    PydanticModel: Type[BaseModel],
    model: str = "gpt-4-0125-preview"
) -> Dict[str, Any]:
    return _extract_json_fields(content, PydanticModel, model)

__all__ = ["Lox", "build_pydantic_model", "extract_json_fields"]