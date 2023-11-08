export LD_LIBRARY_PATH=$(pwd)/WasmEdge/libtorch/lib

# Compile the application to WebAssembly
cd rust/
#cargo clean
cargo build --target=wasm32-wasi --release
cd ..

# Copy the output WASM file
cp rust/target/wasm32-wasi/release/wasmedge-wasinn-example-mobilenet-image.wasm .

ts=$(date +%s%N)
wasmedge --dir .:. wasmedge-wasinn-example-mobilenet-image.wasm models/torchscript_model.pt
echo $((($(date +%s%N) - $ts)/1000000)) ms