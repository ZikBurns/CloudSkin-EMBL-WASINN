# RustLambdaTests
This module has some 

Here is a summary of each Module:
* `RustLambdaTests`: Includes some tests made to try rust in lambda
  * `PipeLambda`: Pipe that sends string from python to rust
  * `PipeLambdaFloat`: Pipe that sends float array from python to rust
  * `PipeLambdaInts`: Pipe that sends int array from python to rust
  * `ReadWrite`: Experiment with reading and writing to and from a pipe
  * `SimpleRustLambda`: Simple code of a rust call from python
* `Wasinn_python_rust`: Python module that transforms images from python and pipes them to rust for them to be inferenced.
  * `main-pipe(-big/-url).py`: Sends a transformed image through the pipe and rust receives it.
  * `main-nopipe.py`: Just calls rust, without sending any image
* `Wasinn_pytorch_rust_RESNET`: Python module that transforms images from python and pipes them to rust for them to be inferenced. Modified version of [WasmEdge example](https://github.com/second-state/WasmEdge-WASINN-examples/tree/master/pytorch-mobilenet-image).
* `wasinn_vs_pytorch`: Collection of tests to both wasi-nn and pytorch using different configurations
  * `batch`: Batch inference using already transformed images
    * `transform_images`: Download and transform the images into npy files. One npy file per transformed image
    * `pytorch`: Reads transformed images and applies inference using pytorch in python
    * `wasinn`: Reads transformed images and applies inference using wasmedge in rust
  * `batch-cpulimit`: Batch inference using already transformed images limiting CPU usage. Doesn't work.
  * `batch-lithops`: Batch inference using already transformed images in local lithops
    * `transform_images`: Download and transform the images into npy files. One npy file per transformed image.
      * `main.py`: Downloads and transforms images
      * `group_images.py`: Groups images into subdirectories. Each subdirectory is a batch. This is like this for Rust to be able to read a whole directory and create a batch from it.
    * `pytorch`: Invokes a lithops function per batch locally. Each function calls pytorch.
    * `wasinn`: Invokes a lithops function per batch locally. Each function calls wasmedge to read transformed images and apply inference.
  * `serial`: Serial inference using already an transformed image
    * `transform_images`: Download and transform an images into a npy file
    * `pytorch`: Reads transforme image and applies inference using pytorch in python
    * `wasinn`: Reads transforme image and applies inference using wasmedge in rust
  * `whole-batch`: Batch inference using already transformed images. The difference with batch is that here, the whole batch of images is a npy file.
    * `transform_images`: Download and transform all the images into 1 big npy file.
    * `pytorch`: Reads npy file and applies batch inference using pytorch in python
    * `wasinn`: Reads npy file and applies inference using wasmedge in rust
* `Wasinn_lambda`: Experiment to execute a lambda, downloading wasinn from S3 and executing wasmedge from the lamdba. Doesn't work as of now.