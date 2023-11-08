import json
import sys
import PIL
import zipfile
import os
import shutil
import requests
import io
import subprocess
import boto3
import zipfile
import stat
import struct
def import_torch():
    torch_dir = '/tmp/python/torch'
    # append the torch_dir to PATH so python can find it
    sys.path.append(torch_dir)
    python_dir = '/opt/python'
    sys.path.append(python_dir)
    if not os.path.exists(torch_dir):
        tempdir = '/tmp/python/_torch'
        if os.path.exists(tempdir):
            shutil.rmtree(tempdir)
        zipfile.ZipFile('/opt/python/torch.zip', 'r').extractall(tempdir)
        os.rename(tempdir, torch_dir)

def download_WasmEdge():
    i=0

import_torch()
from transformations import apply_tfms,normalize
from PIL import Image
from torch import Tensor
from torchvision import transforms

def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    if not os.path.exists('/tmp/wasinn'):
        bucket_name = 'off-sample'
        zip_file_key = 'wasinn-installed.zip'
        local_zip_file_path = '/tmp/wasinn-installed.zip'
        local_extract_directory = '/tmp'
        s3_client.download_file(bucket_name, zip_file_key, local_zip_file_path)
        with zipfile.ZipFile(local_zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(local_extract_directory)
        os.remove(local_zip_file_path)
        command = ['cmake', '--install', '/tmp/wasinn/build']
        subprocess.run(command)
        
    if not os.path.exists('/tmp/wasmedge'):
        bucket_name = 'off-sample'
        zip_file_key = 'wasmedge.zip'
        local_zip_file_path = '/tmp/wasmedge.zip'
        local_extract_directory = '/tmp'
    
        # Download the zip file from S3
        s3_client.download_file(bucket_name, zip_file_key, local_zip_file_path)
        
        subprocess.check_output(['unzip', '-q', local_zip_file_path, '-d', local_extract_directory], stderr=subprocess.STDOUT)
        
        os.remove(local_zip_file_path)
        print(os.listdir("/tmp/.wasmedge"))
        # Specify the directory you want to add to the PATH
        directory_to_add = '/tmp/.wasmedge/bin/wasmedge'
    
        # Get the current value of the PATH variable
        current_path = os.environ.get('PATH', '')
        print(current_path)
        # Add the directory to the PATH
        new_path = f'{directory_to_add}:{current_path}'
        
        # Update the PATH environment variable
        os.environ['PATH'] = new_path
        print(os.environ['PATH'])
        
        # Define the full path to the wasmedge executable
        wasmedge_path = '/tmp/.wasmedge/bin/wasmedge'
        os.chmod(wasmedge_path, stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    # command = f'{wasmedge_path} --version'
    
    # # Execute the command and capture the output
    # result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # # Check the return code
    # if result.returncode == 0:
    #     # Extract the output
    #     output = result.stdout.strip()
    #     print(f"wasmedge version:\n{output}")
    # else:
    #     print(result)
    #     print("Error executing wasmedge command.")
    
    if not os.path.exists('/tmp/libtorch'):
        bucket_name = 'off-sample'
        zip_file_key = 'libtorch.zip'
        local_zip_file_path = '/tmp/libtorch.zip'
        local_extract_directory = '/tmp'
        s3_client.download_file(bucket_name, zip_file_key, local_zip_file_path)
        with zipfile.ZipFile(local_zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(local_extract_directory)
        os.remove(local_zip_file_path)
    
    
    
    if not os.path.exists('/tmp/wasmedge-wasinn-example-mobilenet-image.wasm'):
        bucket_name = 'off-sample'
        zip_file_key = 'wasmedge-wasinn-example-mobilenet-image.wasm'
        local_zip_file_path = '/tmp/wasmedge-wasinn-example-mobilenet-image.wasm'
        s3_client.download_file(bucket_name, zip_file_key, local_zip_file_path)


    directory_path = '/tmp/.wasmedge/lib'

    # Iterate over files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        print(f"Checking file: {file_path}")
        if os.path.islink(file_path):
            target = os.readlink(file_path)
            print(f"Symbolic link: {file_path} --> {target}")
    
    print(os.listdir("/opt"))
    url=event["url"]
    response = requests.get(url).content
    image = Image.open(io.BytesIO(response)).convert('RGB')
    imgtensor = transforms.ToTensor()(image)
    x = apply_tfms(imgtensor, size=224, padding_mode='reflection', mode='bilinear')
    datanormed = normalize(x,mean=Tensor([0.485, 0.456, 0.406]),std=Tensor([0.229, 0.224, 0.225]))
    tensorray= datanormed.numpy()
    reshaped_array = tensorray.reshape(3, -1)
    transposed_array = reshaped_array.transpose()
    flattened=transposed_array.flatten()
    data = struct.pack('<{}f'.format(len(flattened)), *flattened)
    
    shutil.copy("/opt/torchscript_model.pt", "/tmp/torchscript_model.pt")
    print(os.listdir("/tmp"))
    command = '/tmp/.wasmedge/bin/wasmedge --dir .:. wasmedge-wasinn-example-mobilenet-image.wasm torchscript_model.pt'
    os.environ['LD_LIBRARY_PATH'] = f"/tmp/libtorch/lib"
    existing_value = os.environ.get('LD_LIBRARY_PATH')
    new_value = '/tmp/.wasmedge/lib'
    updated_value = f'{existing_value}:{new_value}'
    os.environ['LD_LIBRARY_PATH']=updated_value
    os.environ['Torch_DIR'] = f"/tmp/libtorch"
    proc = subprocess.Popen(command,shell=True, cwd='/tmp', stdin=subprocess.PIPE)
    proc.communicate(data)
    return_code = proc.wait()
    return {
        'statusCode': return_code,
        'body': json.dumps('Hello from Lambda!')
    }
