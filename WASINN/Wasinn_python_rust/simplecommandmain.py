# import wasmtime
# from wasmtime import Store, Module, Instance, loader
# store = Store()
#
# wasmfile='wasmedge-wasinn-example-mobilenet-image.wasm'
# engine = wasmtime.Engine()
#
# wasm_module = wasmtime.Module.from_file(engine,wasmfile)
# instance = wasmtime.Instance(store, wasm_module,[])
# result = instance.exports.my_function("models/torchscript_model.pt", "images/on-sample.png")
#
import subprocess
import os

# Set LD_LIBRARY_PATH environment variable
os.environ['LD_LIBRARY_PATH'] = f"{os.getcwd()}/WasmEdge/libtorch/lib"
command = 'wasmedge --dir .:. wasmedge-wasinn-example-mobilenet-image.wasm models/torchscript_model.pt images/on-sample.png'
subprocess.run(command, shell=True)
