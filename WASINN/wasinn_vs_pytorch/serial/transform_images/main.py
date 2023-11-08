



import io
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
urls=urls[0:5000]


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
numpy.save('data_array.npy', tensorray)
