import os
import subprocess

def lambda_handler(event, context):
    input_string = "Hello from Python!"

    # Invoke the Rust binary and pass the input string as an argument
    result = subprocess.check_output(["./rust_code/target/x86_64-unknown-linux-musl/release/rust_code", input_string])
    with open('/tmp/output.txt', 'r') as f:
        file_contents = f.read()
        print(file_contents)
    # Return a response or perform any other desired actions
    return {
        'statusCode': 200,
        'body': 'Rust execution completed'
    }