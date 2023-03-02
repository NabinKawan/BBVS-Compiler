from fastapi import FastAPI, UploadFile

from app.dtos.command_dto import CommandDto
from app.dtos.execute_dto import ExecuteDto
from app.services import blockchain_service
from app.services.compiler_service import CompilerService
from app.services.status_service import StatusService
from app.settings import configs, BlockchainSettings
import requests

api_settings = configs.api_settings

app = FastAPI()

compiler_service = CompilerService()
status_service = StatusService()


@app.get("/")
async def root():
    return {"api": api_settings.title}


@app.get("/status")
async def check_blockchain_status():
    return compiler_service.check_blockchain_status()


@app.post("/compile")
async def compile_contract(contract_file: UploadFile, data_file: UploadFile):
    return await compiler_service.compile_contract(contract_file, data_file)


@app.post("/execute")
async def execute_contract(execute_data: ExecuteDto):
    return await compiler_service.execute_contract(execute_data)


@app.get("/get_contract")
async def get_contract(contract_address):
    return await compiler_service.execute_contract(contract_address)


