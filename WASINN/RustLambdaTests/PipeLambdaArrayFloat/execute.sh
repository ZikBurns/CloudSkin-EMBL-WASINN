

cd rust_code
cargo clean
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
cd ..

zip -r lambda_function.zip la mbda_function.py rust_code/target/x86_64-unknown-linux-musl/release/rust_code
