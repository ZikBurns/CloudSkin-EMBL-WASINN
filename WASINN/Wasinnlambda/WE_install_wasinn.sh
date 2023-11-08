rm -rf /tmp/wasinn
mkdir /tmp/wasinn
git clone https://github.com/WasmEdge/WasmEdge.git /tmp/wasinn
# Install the PyTorch dependency
cd /tmp/wasinn
export LD_LIBRARY_PATH=/tmp/libtorch/lib
export Torch_DIR=/tmp/libtorch
# Build and install WasmEdge from source
cd /tmp/wasinn
mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DWASMEDGE_PLUGIN_WASI_NN_BACKEND="PyTorch" .. && make -j

# For the WASI-NN plugin, you should install this project.
sudo cmake --install .

