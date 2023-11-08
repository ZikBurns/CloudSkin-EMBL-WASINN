import os
import subprocess

import requests

wasmedgeurl="https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh"
r = requests.get(wasmedgeurl, allow_redirects=True)
print(r.content)
open('/tmp/install.sh', 'wb').write(r.content)
command = "bash /tmp/install.sh -p /tmp/.wasmedge"
process = subprocess.Popen(command, shell=True)

# Wait for the process to complete
process.wait()

# Check the return code
if process.returncode == 0:
    print("Script executed successfully.")
else:
    print("Script execution failed.")
print(os.listdir("/tmp"))