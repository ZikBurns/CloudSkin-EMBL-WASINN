export LD_LIBRARY_PATH=$(pwd)/WasmEdge/libtorch/lib
#export LD_LIBRARY_PATH=$(pwd)/WasmEdge/libtorch/lib:/home/pepe/CLOUDLAB/METASPACE/tempexp/tmp/usr
#export LD_LIBRARY_PATH=$(pwd)/WasmEdge/libtorch/lib:/lib/x86_64-linux-gnu
#export LD_LIBRARY_PATH=/lib64:$(pwd)/WasmEdge/libtorch/lib:$HOME/anaconda3/lib/
#export PYO3_CROSS_LIB_DIR="/usr/lib/python3.10"
export PYO3_CROSS=1
export PYO3_CROSS_PYTHON_VERSION=3.10
export PYO3_PYTHON=/usr/lib/python3.10

# Compile the application to WebAssembly
cd rust/
cargo clean
cargo build --target=wasm32-wasi --release
cd ..

# Copy the output WASM file
cp rust/target/wasm32-wasi/release/wasmedge-wasinn-example-mobilenet-image.wasm .


ts=$(date +%s%N)
wasmedge --dir .:. wasmedge-wasinn-example-mobilenet-image.wasm models/torchscript_model.pt images/
echo $((($(date +%s%N) - $ts)/1000000)) ms