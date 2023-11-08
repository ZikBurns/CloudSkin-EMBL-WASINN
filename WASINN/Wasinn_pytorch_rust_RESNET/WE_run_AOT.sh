
cd WasmEdge/
# This was done not following the tutorial 
# (https://wasmedge.org/book/en/contribute/build_from_src/plugin_wasi_nn.html#build-wasmedge-with-wasi-nn-pytorch-backend)
# The tutorial suggests to do > export LD_LIBRARY_PATH=$(pwd)/libtorch/lib:${LD_LIBRARY_PATH}
# But it only works with:
export LD_LIBRARY_PATH=$(pwd)/libtorch/lib 

cd ..
wasmedgec wasmedge-wasinn-example-mobilenet-image.wasm out.wasm
ts=$(date +%s%N)
wasmedge --dir .:. out.wasm mobilenet.pt input.jpg
echo $((($(date +%s%N) - $ts)/1000000)) ms
