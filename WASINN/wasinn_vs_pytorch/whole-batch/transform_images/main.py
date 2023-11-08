



import io

import numpy
import requests
from torch import Tensor
from torchvision import transforms
from PIL import Image
from transformations import apply_tfms,normalize_batch,normalize
from torch.utils.data.dataloader import default_collate

datasetname="2016-09-21_16h06m49s__6.csv"
with open(datasetname) as f:
    urls=f.read().splitlines()
urls.pop(0)
urls=urls[0:10]
xtensors = []
for url in urls:
    response = requests.get(url).content
    image = Image.open(io.BytesIO(response)).convert('RGB')
    imgtensor = transforms.ToTensor()(image)
    x = apply_tfms(imgtensor, size=224, padding_mode='reflection', mode='bilinear')
    xtensors.append(x.data)
batch = default_collate(xtensors)
datanormed = normalize_batch([batch, Tensor([0, 0])], mean=Tensor([0.485, 0.456, 0.406]),
                                   std=Tensor([0.229, 0.224, 0.225]))
batchnormed = datanormed[0]
tensorray= batchnormed.numpy()
reshaped_array = tensorray.reshape(3, -1)
transposed_array = reshaped_array.transpose()
flattened=transposed_array.flatten()
numpy.save('data_array.npy', tensorray)
