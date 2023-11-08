import os
import subprocess


def lambda_handler(event, context):
    rust_binary_path = "rust_code/target/x86_64-unknown-linux-musl/release/rust_code"
    # Create a pipe
    pipe = subprocess.Popen([rust_binary_path], stdin=subprocess.PIPE)

    # Write a string to the pipe
    message = "Hello, Rust!"
    pipe.communicate(message.encode())

    file_path = "/tmp/output.txt"
    content = ""
    if os.path.exists(file_path):
        print("File exists")
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    else:
        print("File does not exist")

    return {
        'statusCode': 200,
        'body': content
    }