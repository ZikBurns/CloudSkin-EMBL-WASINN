#https://vitalflux.com/pytorch-load-predict-pretrained-resnet-model/
import os
import numpy
import os
import shutil
import subprocess
import lithops
import torch



def my_function(images_path):
    jit_model = torch.jit.load('torchscript_model.pt', torch.device('cpu'))

    # Get a list of all files in the directory
    files = os.listdir(images_path)

    concatenated_tensor = []
    for file in files:
        file_path = os.path.join(images_path, file)  # Get the full file path
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
    probabilities = []
    labels = []
    for i in range(len(pred_probs)):
        probabilities.append(pred_probs[i][0])
        if (preds[i] == 0):
            labels.append('off')
        else:
            labels.append('on')

    pred_list = [{'prob': float(prob), 'label': label} for prob, label in zip(probabilities, labels)]
    return pred_list

if __name__ == '__main__':
    groups_path = "images-groups"
    files = os.listdir(groups_path)
    destination_directories = []
    for file in files:
        destination_directories.append(groups_path + "/" + file)
    fexec = lithops.FunctionExecutor(runtime_memory=3008)
    fexec.map(my_function, destination_directories)
    results = fexec.get_result()
    print(results)
    with open("results.txt", "a") as file:
        file.write(str(results)+"\n")