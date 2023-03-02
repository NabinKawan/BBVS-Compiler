from pydantic import BaseModel

from app.dtos.command_dto import CommandDto


class ExecuteDto(BaseModel):
    contract_address: str
    command_params: CommandDto
