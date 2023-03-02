from pydantic import BaseModel
from typing import List


class CommandDto(BaseModel):
    command: str
    option_name: str
    args: List[str]
