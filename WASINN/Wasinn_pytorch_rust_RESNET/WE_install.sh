rm -rf WasmEdge/

# Compile the application to WebAssembly
cd rust/
cargo clean
cargo build --target=wasm32-wasi --release
cd ..

# Copy the output WASM file 
cp rust/target/wasm32-wasi/release/wasmedge-wasinn-example-mobilenet-image.wasm .

# To speed up the image processing, we enable the AOT mode in WasmEdge
wasmedgec rust/target/wasm32-wasi/release/wasmedge-wasinn-example-mobilenet-image.wasm wasmedge-wasinn-example-mobilenet-image-aot.wasm

# Generate the model fixture mobilenet.pt. Use python 3.7 to execute this. It doesn't work with Python 3.10
conda activate python37
python3 -m pip install simpy torch==1.8.2 torchvision==0.9.2 pillow --extra-index-url https://download.pytorch.org/whl/lts/1.8/cpu
python3 gen_resnet_model.py
# If Python 3.10 or other, download mobilenet.pt online
#curl -sLO https://github.com/second-state/WasmEdge-WASINN-examples/raw/master/pytorch-mobilenet-image/mobilenet.pt

# Download image
curl -sL -o input.jpg https://github.com/bytecodealliance/wasi-nn/raw/main/rust/examples/images/1.jpg

# Generate raw Tensor
python3 gen_tensor.py input.jpg image-1x3x224x224.rgb

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
