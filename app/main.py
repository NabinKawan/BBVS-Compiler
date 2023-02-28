from fastapi import FastAPI, UploadFile
from app.services.compiler_service import CompilerService
from app.services.status_service import StatusService
from app.settings import configs

api_settings = configs.api_settings

app = FastAPI()

compiler_service = CompilerService()
status_service = StatusService()


@app.get("/")
async def root():
    return {"api": api_settings.title}


# @app.get("/status")
# async def check_blockchain_status():
#     return status_service.test_ping('http://localhost:5005')


@app.post("/compile")
async def compile_contract(contract_file: UploadFile, data_file: UploadFile):
    return await compiler_service.compile_contract(contract_file, data_file)
