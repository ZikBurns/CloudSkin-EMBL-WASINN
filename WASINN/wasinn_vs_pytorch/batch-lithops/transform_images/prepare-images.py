import os
import shutil
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
origin_directory="images"
final_directory="images-groups"
files_per_directory=10
files = os.listdir(origin_directory)
num_subdirectories = (len(files) + files_per_directory - 1) // files_per_directory
if os.path.exists(final_directory):
    shutil.rmtree(final_directory)
if not os.path.exists(final_directory):
    os.mkdir(final_directory)
for i in range(num_subdirectories):
    os.makedirs(os.path.join(final_directory, f"subdir_{i}"), exist_ok=True)
destination_directories=[]
for i, filename in enumerate(files):
    source_path = os.path.join(origin_directory, filename)
    destination_directory = os.path.join(final_directory, f"subdir_{i % num_subdirectories}")
    destination_path = os.path.join(destination_directory, filename)
    if destination_directory not in destination_directories:
        destination_directories.append(destination_directory)
    shutil.copy2(source_path, destination_path)
if os.path.exists("../wasinn/images-groups"):
    shutil.rmtree("../wasinn/images-groups")
if os.path.exists("../pytorch/images-groups"):
    shutil.rmtree("../pytorch/images-groups")
copytree(final_directory, "../wasinn/images-groups")
copytree(final_directory, "../pytorch/images-groups")