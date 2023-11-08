use std::{
    fs::File,
    io::{self, Write},
    os::unix::io::FromRawFd,
};

fn main() -> io::Result<()> {
    let mut f = unsafe { File::from_raw_fd(7) };
    write!(&mut f, "Hello world!")?;
    Ok(())
}