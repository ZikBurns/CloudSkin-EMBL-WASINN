rm -rf WasmEdge/ 

#rm -rf mobilenet.pt 
rm -rf wasmedge-wasinn-example-mobilenet-image.wasm 
rm -rf wasmedge-wasinn-example-mobilenet-image-aot.wasm 
rm -rf image-1x3x224x224.rgb

cd rust/
cargo clean
