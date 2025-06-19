from pydantic import BaseModel
from typing import List

class ConditionInfo(BaseModel):
    name: str
    title: str
    description: str
    causes: List[str]
    symptoms: List[str]
    treatment: List[str]
    prevention: List[str]
    image: str 