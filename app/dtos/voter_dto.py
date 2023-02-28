from pydantic import BaseModel
from typing import List


class VoterDto(BaseModel):
    voter_id: str
    name: str
    voted_to: List[str]
    is_voted: bool

