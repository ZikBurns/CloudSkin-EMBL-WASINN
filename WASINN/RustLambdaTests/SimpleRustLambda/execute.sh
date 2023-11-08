

cd rust_code
cargo build --release --target x86_64-unknown-linux-musl
cd ..

zip -r lambda_function.zip lambda_function.py rust_code/target/x86_64-unknown-linux-musl/release/rust_code
