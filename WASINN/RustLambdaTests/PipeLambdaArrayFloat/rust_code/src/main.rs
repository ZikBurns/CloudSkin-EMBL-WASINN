
use std::io::{self, Read};
use std::fs::File;
use std::io::Write;
use std::mem;
use std::time::{SystemTime, UNIX_EPOCH};

fn main() -> io::Result<()> {
        // Read from stdin (pipe)
    let mut buffer = Vec::new();
    io::stdin().read_to_end(&mut buffer)?;

    // Interpret the byte array as an array of little-endian integers
    let numbers: &[f32] = unsafe {
        let len = buffer.len() / mem::size_of::<f32>();
        let ptr = buffer.as_ptr() as *const f32;

        std::slice::from_raw_parts(ptr, len)
    };

    // Process the input (numbers)
    let result: Vec<f32> = numbers.iter().map(|&x| x ).collect();
        // Get the current time
    let now = SystemTime::now();

    // Calculate the duration since the Unix epoch
    let duration = now.duration_since(UNIX_EPOCH).expect("Failed to retrieve duration");

    // Convert the duration to seconds with fractional parts
    let seconds = duration.as_secs() as f64 + duration.subsec_nanos() as f64 * 1e-9;

    println!("Current time: {:.6}", seconds);
    // Print the output (result)
    for num in &result {
        println!("{}", num);
    }

    Ok(())
}