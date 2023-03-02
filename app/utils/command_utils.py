import subprocess

from app.dtos.execute_dto import ExecuteDto


def run_command(exe_params: ExecuteDto):
    cmd_params = exe_params.command_params
    if len(cmd_params.option_name)==0:
        print("check")
        val = subprocess.run(
            ["python", "contract.py", cmd_params.command], stdout=subprocess.PIPE, text=True)
    else:
        val = subprocess.run(
            ["python", "contract.py", cmd_params.command, cmd_params.option_name,
             *exe_params.command_params.args], stdout=subprocess.PIPE, text=True)
    print(val.stdout)
    return val.stdout
