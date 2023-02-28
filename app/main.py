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


@app.get("/status")
async def check_blockchain_status():
    return status_service.test_ping('http://192.168.56.1:5005')


@app.post("/bytecode")
async def generate_bytecode(file: UploadFile):
    return await compiler_service.generate_bytecode(file)
# @app.post("/bytecode")
# def compile(bytecode: str, data_provider: Dict[str, Any]):
#     return compiler_service.generate_bytecode(code)
