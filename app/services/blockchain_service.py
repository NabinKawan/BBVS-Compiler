import requests
import json

from app.settings import configs

blockchain_settings = configs.blockchain_settings

blockchain_url = f'http://{blockchain_settings.host}:{blockchain_settings.port}'


class BlockchainService:

    @staticmethod
    def add_contract(tx):
        response = requests.post(f'{blockchain_url}/add_contract', data=json.dumps(tx),
                                 headers={'Content-type': 'application/json'})
        return response.json()

    @staticmethod
    def update_contract(tx):
        response = requests.post(f'{blockchain_url}/update_contract', data=json.dumps(tx),
                                 headers={'Content-type': 'application/json'})
        return response.json()

    @staticmethod
    def get_blockchain_status():
        response = requests.get(f'{blockchain_url}/status')
        return response.json()

    @staticmethod
    async def get_contract_data(contract_address: str):
        response = requests.get(f'{blockchain_url}/blocks/{contract_address}')
        data = response.json()
        contract_data = data['tx']['contract_data']
        return json.loads(contract_data)
