
# This was done not following the tutorial 
# (https://wasmedge.org/book/en/contribute/build_from_src/plugin_wasi_nn.html#build-wasmedge-with-wasi-nn-pytorch-backend)
# The tutorial suggests to do > export LD_LIBRARY_PATH=$(pwd)/libtorch/lib:${LD_LIBRARY_PATH}
# But it only works with:
export LD_LIBRARY_PATH=$(pwd)/WasmEdge/libtorch/lib 


ts=$(date +%s%N)
wasmedge --dir .:. wasmedge-wasinn-example-mobilenet-image.wasm models/torchscript_model.pt images
echo $((($(date +%s%N) - $ts)/1000000)) ms