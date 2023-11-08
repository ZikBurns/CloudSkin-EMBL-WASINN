


import subprocess
import os
import struct

rust_binary_path = "rust_code/target/x86_64-unknown-linux-musl/release/rust_code"
# Create a pipe
pipe = subprocess.Popen([rust_binary_path], stdin=subprocess.PIPE)

# Write a string to the pipe
numbers = [5,2,3,4,5]
data = struct.pack('<{}i'.format(len(numbers)), *numbers)

# Write the byte array to the pipe
pipe.communicate(data)

# file_path = "/tmp/output.txt"
#
# if os.path.exists(file_path):
#     print("File exists")
#     with open(file_path, 'r') as file:
#         content = file.read()
#         print(content)
# else:
#     print("File does not exist")