from pydantic import BaseModel
from typing import List


class CandidateDto(BaseModel):
    candidate_id: str
    name: str
    image_url: str
    logo: str
    post: str
