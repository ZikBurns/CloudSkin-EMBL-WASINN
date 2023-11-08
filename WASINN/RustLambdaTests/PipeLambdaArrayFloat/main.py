


import subprocess
import os
import struct
import time

rust_binary_path = "rust_code/target/x86_64-unknown-linux-musl/release/rust_code"
# Create a pipe
pipe = subprocess.Popen([rust_binary_path], stdin=subprocess.PIPE)

# Write a string to the pipe
numbers = []
data = struct.pack('<{}f'.format(len(numbers)), *numbers)
start_time = time.time()
print("Start time", start_time)
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