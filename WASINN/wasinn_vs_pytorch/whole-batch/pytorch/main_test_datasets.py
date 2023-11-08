#https://vitalflux.com/pytorch-load-predict-pretrained-resnet-model/
import base64
import io
import json
from PIL import Image
from torch import Tensor
from torch.utils.data.dataloader import default_collate
from torchvision import transforms
import torch
import requests
import numpy

jit_model = torch.jit.load('torchscript_model.pt',torch.device('cpu'))
numpy_array=numpy.load("../transform_images/data_array.npy")
batch_normed = torch.from_numpy(numpy_array)

# resnet.eval()
with torch.no_grad():
    out = jit_model.forward(batch_normed)
out = torch.softmax(out, dim=1)
pred_probs = out.numpy()
preds = pred_probs.argmax(axis=1)

probabilities=[]
labels=[]
for i in range(len(pred_probs)):
    probabilities.append(pred_probs[i][0])
    if (preds[i] == 0):
        labels.append('off')
    else:
        labels.append('on')

pred_list = [{'prob': float(prob), 'label': label} for prob, label in zip(probabilities, labels)]
print(pred_list)

