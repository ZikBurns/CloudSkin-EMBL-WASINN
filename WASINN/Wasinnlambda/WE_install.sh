

rm -rf /tmp/wasinn

curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash -s -- -p /tmp/.wasmedge
mkdir /tmp/wasinn
git clone https://github.com/WasmEdge/WasmEdge.git /tmp/wasinn/WasmEdge
# Install the PyTorch dependency
cd /tmp/wasinn/WasmEdge
export PYTORCH_VERSION="1.5.1"
curl -s -L -O --remote-name-all https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip
#curl -s -L -O --remote-name-all https://download.pytorch.org/libtorch/lts/1.8/cpu/libtorch-cxx11-abi-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip
unzip -q "libtorch-cxx11-abi-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip"
rm -f "libtorch-cxx11-abi-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip"
export LD_LIBRARY_PATH=/tmp/wasinn/WasmEdge/libtorch/lib
export Torch_DIR=/tmp/wasinn/WasmEdge/libtorch


# Build and install WasmEdge from source
cd /tmp/wasinn/WasmEdge
mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DWASMEDGE_PLUGIN_WASI_NN_BACKEND="PyTorch" .. && make -j

# For the WASI-NN plugin, you should install this project.
#sudo cmake --install .

