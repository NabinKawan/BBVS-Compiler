import json
import py_compile
import subprocess
import requests

from app.utils.command_utils import run_command

from app.dtos.command_dto import CommandDto
from app.dtos.execute_dto import ExecuteDto
from app.services.blockchain_service import BlockchainService
from app.settings import configs
from app.utils.file_utils import write_json_to_file, read_json_from_file

blockchain_service = BlockchainService()
blockchain_settings = configs.blockchain_settings

blockchain_url = f'http://{blockchain_settings.host}:{blockchain_settings.port}'


class CompilerService:

    @staticmethod
    async def compile_contract(contract_file, data_file):
        contract_contents = await contract_file.read()
        data_contents = await data_file.read()

        data = data_contents.decode()
        print(json.loads(data))
        clean_data = data.replace('\t', '').replace('\n', '').replace('\r', '')
        write_json_to_file('contract_data.json', json.loads(data))
        byte_code = compile(contract_contents.decode(), 'filename', 'exec').co_code
        tx = {'tx': {'byte_code': str(byte_code), 'contract_data': clean_data}}
        # store to blockchain
        return blockchain_service.add_contract(tx)

    @staticmethod
    async def execute_contract(exe_params: ExecuteDto):
        contract_address = exe_params.contract_address
        data = await blockchain_service.get_contract_data(contract_address)
        write_json_to_file('contract_data.json', data)
        # clean_exe_params = exe_params.command_params.args.replace('\"', '').replace(' ', '_')

        return_value = run_command(exe_params)

        contract_data = read_json_from_file('contract_data.json')
        tx = {'contract_address': contract_address, 'contract_data': json.dumps(contract_data),
              'inputs': exe_params.command_params.json()}
        blockchain_response = await blockchain_service.update_contract(tx)
        response = {'contract_response': return_value.replace('\n', ''), 'blockchain_response': blockchain_response}
        print("return: ", return_value)
        return response

    @staticmethod
    def check_blockchain_status():
        return blockchain_service.get_blockchain_status()
