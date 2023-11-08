use std::{
    fs::File,
    io::{self, Read, BufReader},
    os::unix::io::FromRawFd,
};

fn main() -> io::Result<()> {
    let mut f = unsafe { File::from_raw_fd(6) };
    let mut input = String::new();
    let mut reader = BufReader::new(f);

    reader.read_to_string(&mut input)?;

    println!("I read: {}", input);

    Ok(())
}