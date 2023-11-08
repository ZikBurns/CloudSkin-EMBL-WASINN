#https://vitalflux.com/pytorch-load-predict-pretrained-resnet-model/

import numpy

import torch


jit_model = torch.jit.load('torchscript_model_1.13.pt',torch.device('cpu'))

numpy_array=numpy.load("../transform_images/data_array.npy")
datanormed = torch.from_numpy(numpy_array)
batch_img_tensor = torch.unsqueeze(datanormed, 0)
# resnet.eval()
with torch.no_grad():
    out = jit_model.forward(batch_img_tensor)
softmaxed = torch.softmax(out, dim=1)
pred_probs = softmaxed.numpy()
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
