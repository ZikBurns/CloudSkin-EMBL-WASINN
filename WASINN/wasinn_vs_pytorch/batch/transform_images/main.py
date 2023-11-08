



import io
import os
import shutil
import numpy
import requests
from torch import Tensor
from torchvision import transforms
from PIL import Image
from transformations import apply_tfms,normalize_batch,normalize

datasetname="2016-09-21_16h06m49s__6.csv"
with open(datasetname) as f:
    urls=f.read().splitlines()
urls.pop(0)
urls=urls[0:10]
shutil.rmtree('images')
os.mkdir('images')

for url in urls:
    response = requests.get(url).content
    name_image = url.split("/")[-1]
    image = Image.open(io.BytesIO(response)).convert('RGB')
    imgtensor = transforms.ToTensor()(image)
    x = apply_tfms(imgtensor, size=224, padding_mode='reflection', mode='bilinear')
    datanormed = normalize(x, mean=Tensor([0.485, 0.456, 0.406]), std=Tensor([0.229, 0.224, 0.225]))
    tensorray = datanormed.numpy()
    reshaped_array = tensorray.reshape(3, -1)
    transposed_array = reshaped_array.transpose()
    flattened = transposed_array.flatten()
    numpy.save("images/"+name_image+".npy", tensorray)
destination_dir = os.path.join('..','wasinn/images')
if os.path.exists(destination_dir):
    shutil.rmtree(destination_dir)
shutil.copytree('images', destination_dir)
