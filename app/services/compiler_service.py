import py_compile


class CompilerService:

    @staticmethod
    async def generate_bytecode(file):
        contents = await file.read()
        with open('contract.py', 'w') as f:
            f.write(contents.decode())
        py_compile.compile('contract.py')
        return 'Byte code generated'
        # return py_compile.compile('main.py')

    # @staticmethod
    # def compile_bytecode(bytecode:str,data_provider:Dict[str,Any]):
    #     pass
