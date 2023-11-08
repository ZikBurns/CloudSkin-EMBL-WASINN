import os
import shutil
import subprocess
import lithops
def my_function(images_path):
    os.environ['LD_LIBRARY_PATH'] = f"{os.getcwd()}/WasmEdge/libtorch/lib"
    command = 'wasmedge --dir .:. wasmedge-wasinn-example-mobilenet-image-aot.wasm models/torchscript_model.pt '+images_path

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print("Command output:")
        lines=result.stdout.split("\n")
        result_lines=[]
        for line in lines:
            if line.startswith("RESULT"):
                result_lines.append(line)
        return result_lines
    else:
        # Command execution failed
        print("Command error:")
        print(result.stderr)


if __name__ == '__main__':
    groups_path="images-groups"
    files = os.listdir(groups_path)
    destination_directories=[]
    for file in files:
        destination_directories.append(groups_path+"/"+file)
    fexec = lithops.FunctionExecutor(runtime_memory=3008)
    fexec.map(my_function, destination_directories)

    results = fexec.get_result()
    print(results)
    with open("results.txt", "a") as file:
        file.write(str(results)+"\n")


