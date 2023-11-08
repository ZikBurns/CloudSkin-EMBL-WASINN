
use std::io::{self, Read};
use std::fs::File;
use std::io::Write;

fn main() -> io::Result<()> {
    // Read from stdin (pipe)
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer)?;

    // Process the input
    let result = buffer.to_uppercase();

    // Print the output
    println!("{}", result);

    let mut file = File::create("/tmp/output.txt").expect("Failed to create file");
    file.write_all(result.as_bytes()).expect("Failed to write to file");

    Ok(())
}