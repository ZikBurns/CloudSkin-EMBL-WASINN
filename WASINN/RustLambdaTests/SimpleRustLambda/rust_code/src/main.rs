use std::env;
use std::fs::File;
use std::io::Write;

fn main() {
    // Read the input string from command-line arguments
    let args: Vec<String> = env::args().collect();
    let input_string = &args[1];

    // Process the input (you can perform any desired computation here)
    let processed_output = process_input(input_string);

    // Write the processed output to the /tmp/output.txt file
    let mut file = File::create("/tmp/output.txt").expect("Failed to create file");
    file.write_all(processed_output.as_bytes()).expect("Failed to write to file");
}

fn process_input(input: &str) -> String {
    input.to_uppercase()
}