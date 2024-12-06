from typing import List, Type
from pydantic import BaseModel

def build_pydantic_model(fields: List[str]) -> Type[BaseModel]: ... 