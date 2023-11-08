import io
import struct
import subprocess
import os
import time

import requests
from torch import Tensor
from torchvision import transforms
from PIL import Image


from transformations import apply_tfms,normalize_batch,normalize


url="https://s3.eu-west-1.amazonaws.com/sm-image-storage-prod/iso/2016-09-21_16h06m49s/28aa128e8a38d7d6af1ee8ba367f5c2f"
response = requests.get(url).content
image = Image.open(io.BytesIO(response)).convert('RGB')
imgtensor = transforms.ToTensor()(image)
x = apply_tfms(imgtensor, size=224, padding_mode='reflection', mode='bilinear')
datanormed = normalize(x,mean=Tensor([0.485, 0.456, 0.406]),std=Tensor([0.229, 0.224, 0.225]))
tensorray= datanormed.numpy()
reshaped_array = tensorray.reshape(3, -1)
transposed_array = reshaped_array.transpose()
flattened=transposed_array.flatten()

five=flattened[:5]
data = struct.pack('<{}f'.format(len(flattened)), *flattened)
# Set LD_LIBRARY_PATH environment variable
os.environ['LD_LIBRARY_PATH'] = f"{os.getcwd()}/WasmEdge/libtorch/lib"
command = 'wasmedge --dir .:. wasmedge-wasinn-example-mobilenet-image.wasm models/torchscript_model.pt images/bigimage.png'
start_time = time.time()
print("Start time", start_time)
# subprocess.run(command, shell=True)
proc = subprocess.Popen(command,shell=True, stdin=subprocess.PIPE)
start_time = time.time()
print("Popen time", start_time)
proc.communicate(data)
return_code = proc.wait()
end_time = time.time()
print("Final pipe time", end_time)
# Print the return code
print("Return code:", return_code)


