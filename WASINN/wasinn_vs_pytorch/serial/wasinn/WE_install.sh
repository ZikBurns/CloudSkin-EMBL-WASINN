rm -rf WasmEdge/

# Compile the application to WebAssembly
cd rust/
cargo clean
cargo build --target=wasm32-wasi --release
cd ..

# Copy the output WASM file 
cp rust/target/wasm32-wasi/release/wasmedge-wasinn-example-mobilenet-image.wasm .


# Get the Source Code
git clone https://github.com/WasmEdge/WasmEdge.git
cd WasmEdge

# Install the PyTorch dependency
export PYTORCH_VERSION="1.8.2"
curl -s -L -O --remote-name-all https://download.pytorch.org/libtorch/lts/1.8/cpu/libtorch-cxx11-abi-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip
unzip -q "libtorch-cxx11-abi-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip"
rm -f "libtorch-cxx11-abi-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip"
export LD_LIBRARY_PATH=$(pwd)/libtorch/lib
export Torch_DIR=$(pwd)/libtorch

# Build and install WasmEdge from source
mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DWASMEDGE_PLUGIN_WASI_NN_BACKEND="PyTorch" .. && make -j

# For the WASI-NN plugin, you should install this project.
sudo cmake --install .
