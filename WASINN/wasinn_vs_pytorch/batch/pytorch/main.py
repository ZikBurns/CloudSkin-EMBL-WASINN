#https://vitalflux.com/pytorch-load-predict-pretrained-resnet-model/
import os

import numpy

import torch


jit_model = torch.jit.load('torchscript_model.pt',torch.device('cpu'))
directory = '../transform_images/images'  # Specify the directory path

# Get a list of all files in the directory
files = os.listdir(directory)

concatenated_tensor=[]
for file in files:
    file_path = os.path.join(directory, file)  # Get the full file path
    if os.path.isfile(file_path):  # Check if it's a file
        numpy_array = numpy.load(file_path)
        tensorized = torch.from_numpy(numpy_array)
        batch_img_tensor = torch.unsqueeze(tensorized, 0)
        concatenated_tensor.append(batch_img_tensor)


concatenated_tensor = torch.cat(concatenated_tensor, dim=0)


# resnet.eval()
with torch.no_grad():
    out = jit_model.forward(concatenated_tensor)
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
