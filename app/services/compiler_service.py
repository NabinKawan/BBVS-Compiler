import py_compile


class CompilerService:

    @staticmethod
    async def compile_contract(contract_file, data_file):
        contract_contents = await contract_file.read()
        data_contents = await data_file.read()
        data = data_contents.decode()
        byte_code = compile(contract_contents.decode(), 'filename', 'exec').co_code
        return {'byte_code': f'{byte_code}', 'data': data}