import subprocess
from app.settings import configs

blockchain_settings = configs.blockchain_settings

class StatusService:
    def test_ping(self, api_url):
        # Construct the ping command
        command = ['ping', '-c', '1', api_url]

        # Execute the command and capture the output
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        # Check the return code to see if the ping was successful
        if process.returncode == 0:
            return f'{blockchain_settings.name} connected'
        else:
            return "No blockchain connected"
