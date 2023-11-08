
use std::io::{self, Read};
use std::fs::File;
use std::io::Write;
use std::mem;

fn main() -> io::Result<()> {
        // Read from stdin (pipe)
    let mut buffer = Vec::new();
    io::stdin().read_to_end(&mut buffer)?;

    // Interpret the byte array as an array of little-endian integers
    let numbers: &[i32] = unsafe {
        let len = buffer.len() / mem::size_of::<i32>();
        let ptr = buffer.as_ptr() as *const i32;

        std::slice::from_raw_parts(ptr, len)
    };

    // Process the input (numbers)
    let result: Vec<i32> = numbers.iter().map(|&x| x ).collect();

    // Print the output (result)
    for num in &result {
        println!("{}", num);
    }

    Ok(())
}