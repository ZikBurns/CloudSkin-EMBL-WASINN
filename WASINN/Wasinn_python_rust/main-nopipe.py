import struct
import subprocess
import os
import time

from torch import Tensor
from torchvision import transforms
from PIL import Image
from transformations import apply_tfms,normalize_batch,normalize

# Set LD_LIBRARY_PATH environment variable
os.environ['LD_LIBRARY_PATH'] = f"{os.getcwd()}/WasmEdge/libtorch/lib"
command = 'wasmedge --dir .:. nopipe.wasm models/torchscript_model.pt images/bigimage.png'
start_time = time.time()
print("Start time", start_time)
subprocess.run(command, shell=True)
# subprocess.Popen(command, shell=True, stdin=subprocess.DEVNULL)
