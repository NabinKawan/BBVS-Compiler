import subprocess
from fastapi import HTTPException
from app.dtos.execute_dto import ExecuteDto
from fastapi.responses import JSONResponse


def run_command(exe_params: ExecuteDto):
    cmd_params = exe_params.command_params
    if len(cmd_params.option_name) == 0:
        val = subprocess.run(
            ["python", "bbvs_contract.py", cmd_params.command], stdout=subprocess.PIPE, text=True)
    else:
        val = subprocess.run(
            ["python", "bbvs_contract.py", cmd_params.command, cmd_params.option_name,
             *exe_params.command_params.args], stdout=subprocess.PIPE, text=True)

    if val.returncode:
        err = val.stdout.replace("\n", "")
        raise HTTPException(status_code=400, detail=err)
    return val.stdout
