use image;
use std::convert::TryInto;
use std::env;
use std::fs;
use std::fs::File;
use std::io::Read;
use wasi_nn;
mod imagenet_classes;
use std::str;

pub fn main() {
    main_entry();
}

#[no_mangle]
fn main_entry() {
    infer_image();
}

fn infer_image() {
    let args: Vec<String> = env::args().collect(); //Gets arguments from command line
    let model_bin_name: &str = &args[1]; // File name for the pytorch model
    let image_name: &str = &args[2]; // File name for the input image

    let weights = fs::read(model_bin_name).unwrap(); //Read the entire contents of a file into a bytes vector. -> Result<Vec<u8>>. Unwrap crashes the program if result contains an Error
    println!("Read torchscript binaries, size in bytes: {}", weights.len());
    //weights is a Vec<u8>
    // load model using one (or more) opaque byte arrays
    /*
    pub unsafe fn load(
        builder: GraphBuilderArray<'_>, // pub type GraphBuilderArray<'a> = &'a [GraphBuilder<'a>]; (The 'a reads ‘the lifetime a’)
                                        // pub type GraphBuilder<'a> = &'a [u8];                    (u8 is the 8-bit unsigned integer type.)
        encoding: GraphEncoding, 
        target: ExecutionTarget
    ) -> Result<Graph, NnErrno>
     */

    let graph = unsafe { //  Although the code might be okay, if the Rust compiler doesn’t have enough information to be confident, it will reject the code. In these cases, you can use unsafe code to tell the compiler, “Trust me, I know what I’m doing.”
        wasi_nn::load(
            &[&weights],  
            wasi_nn::GRAPH_ENCODING_PYTORCH, //GRAPH_ENCODING_ONNX | GRAPH_ENCODING_OPENVINO | GRAPH_ENCODING_PYTORCH | GRAPH_ENCODING_TENSORFLOW | GRAPH_ENCODING_TENSORFLOWLITE
            wasi_nn::EXECUTION_TARGET_CPU, // EXECUTION_TARGET_CPU | EXECUTION_TARGET_GPU | EXECUTION_TARGET_TPU
        )
        .unwrap()
    };
    println!("Loaded graph into wasi-nn with ID: {}", graph);

    // initialize the computation context
    /*
    pub unsafe fn init_execution_context(
        graph: Graph
    ) -> Result<GraphExecutionContext, NnErrno> // pub type GraphExecutionContext = u32 (u32 is the 32-bit unsigned integer type.);
*/
    let context = unsafe { wasi_nn::init_execution_context(graph).unwrap() };
    println!("Created wasi-nn execution context with ID: {}", context);

    // Load a tensor that precisely matches the graph input tensor (see below)
    let tensor_data = image_to_tensor(image_name.to_string(), 224, 224); //tensor_data = Vec<u8>
    println!("Read input tensor, size in bytes: {}", tensor_data.len());
    /*
    pub struct Tensor<'a> {
        pub dimensions: TensorDimensions<'a>, // pub type TensorDimensions<'a> = &'a [u32];
        pub type_: TensorType, //TENSOR_TYPE_F16 | TENSOR_TYPE_F32 | TENSOR_TYPE_I32 | TENSOR_TYPE_U8
        pub data: TensorData<'a>, // pub type TensorData<'a> = &'a [u8];
    }
     */
    let tensor = wasi_nn::Tensor {
        dimensions: &[1, 3, 224, 224],
        type_: wasi_nn::TENSOR_TYPE_F32, 
        data: &tensor_data,
    };

    // set_input to bind tensor to the execution context
    /*
    pub unsafe fn set_input(
        context: GraphExecutionContext,
        index: u32,
        tensor: Tensor<'_>
    ) -> Result<(), NnErrno>
    */
    unsafe {
        wasi_nn::set_input(context, 0, tensor).unwrap(); 
    }

    // Execute the inference.
    unsafe {
        wasi_nn::compute(context).unwrap();
    }
    println!("Executed graph inference");

    // Retrieve the inference result tensors / output
    let mut output_buffer = vec![0f32; 1000]; //vector with 0s in 1000 positions
    unsafe {
        /*
        pub unsafe fn get_output(
            context: GraphExecutionContext,
            index: u32,
            out_buffer: *mut u8,
            out_buffer_max_size: BufferSize
        ) -> Result<BufferSize, NnErrno>
         */
        wasi_nn::get_output(
            context,
            0,
            &mut output_buffer[..] as *mut [f32] as *mut u8, // Must be u8
            (output_buffer.len() * 4).try_into().unwrap(), //f32/8 = 4
        )
        .unwrap();
    }


    //Finally, we sort the output and then print the top-5 classification result
    let results = sort_results(&output_buffer);

    for i in 0..5 {
        println!(
            "   {}.) [{}]({:.4}){}",
            i + 1,
            results[i].0,
            results[i].1,
            imagenet_classes::IMAGENET_CLASSES[results[i].0]
        );
    }
}

// Sort the buffer of probabilities. The graph places the match probability for each class at the
// index for that class (e.g. the probability of class 42 is placed at buffer[42]). Here we convert
// to a wrapping InferenceResult and sort the results.
fn sort_results(buffer: &[f32]) -> Vec<InferenceResult> {
    let mut results: Vec<InferenceResult> = buffer
        .iter()
        .enumerate()
        .map(|(c, p)| InferenceResult(c, *p))
        .collect();
    results.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    results
}

// let tensor_data = image_to_tensor(image_name.to_string(), 224, 224); 
// Take the image located at 'path', open it, resize it to height x width, and then converts
// the pixel precision to FP32. The resulting BGR pixel vector is then returned.
fn image_to_tensor(path: String, height: u32, width: u32) -> Vec<u8> {
    let mut file_img = File::open(path).unwrap();
    let mut img_buf = Vec::new(); // Vec is a growable array type (like a buffer) and is mutable
    // Read all bytes until EOF in this source, placing them into img_buf.
    file_img.read_to_end(&mut img_buf).unwrap(); //fn read_to_end(&mut self, buf: &mut Vec<u8>) -> Result<usize>
    // Create a new image from a byte slice (&mut Vec<u8> is converted into &[u8])
    let img = image::load_from_memory(&img_buf).unwrap().to_rgb8(); //pub fn load_from_memory(buffer: &[u8]) -> ImageResult<DynamicImage>
    // DynamicImage img represents a matrix of pixels which are convertible from and to an RGBA representation. 
    /*
    Image sampling Resize the supplied image to the specified dimensions. 
    nwidth and nheight are the new dimensions. 
    filter is the sampling filter to use.
    pub fn resize<I: GenericImageView>(
        image: &I, //reference to Image
        nwidth: u32, 
        nheight: u32, 
        filter: FilterType 
    ) -> ImageBuffer< 
            I::Pixel, //A generalized pixel. A pixel object is usually not used standalone but as a view into an image buffer.
            Vec<<I::Pixel as Pixel>::Subpixel> //The scalar type that is used to store each channel in this pixel (u8, u16, f32)
        >
     */
    let resized =
        image::imageops::resize(
            &img, 
            height, 
            width, 
            ::image::imageops::FilterType::Triangle
        );
    
    //
    let mut flat_img: Vec<f32> = Vec::new(); //growable vector

    for rgb in resized.pixels() {
        //println!("{}, {}, {}",rgb[0], rgb[1], rgb[2]); // rgb[0] = red, rgb[1]=green, rgb[2]=blue
        flat_img.push((rgb[0] as f32 / 255. - 0.485) / 0.229);
        flat_img.push((rgb[1] as f32 / 255. - 0.456) / 0.224);
        flat_img.push((rgb[2] as f32 / 255. - 0.406) / 0.225);
    }
    /*for index in 0..flat_img.len(){
        println!("{}",flat_img[index]);
    }*/
    println!("{}",flat_img.len());
    let bytes_required = flat_img.len() * 4; // Is multiplied by 4 because is a type f32 (32/8=4)
    let mut u8_f32_arr: Vec<u8> = vec![0; bytes_required]; //vec! is the same as Vec::new(); but this case has zeroes in bytes_required positions

    for c in 0..3 { //For c = 0, 1, 2
        for i in 0..(flat_img.len() / 3) { //for each RGB
            let u8_f32: f32 = flat_img[i * 3 + c] as f32; // [0, 3, 6, 9... 1, 4, 7, 10...2, 5, 8, 11...]
            /*if i < 100 {
                println!("{}", u8_f32)
            }*/
            let u8_bytes = u8_f32.to_ne_bytes(); //https://doc.rust-lang.org/std/primitive.f32.html#method.to_ne_bytes f32 is converted into [u8:4] (array unsigned int with 4 positions)
            /*if i < 100 {
                println!("{} {} {} {}", u8_bytes[0], u8_bytes[1], u8_bytes[2], u8_bytes[3])
            }*/
            for j in 0..4 { // for each position of u8_bytes
                /*let pos=((flat_img.len() / 3 * c + i) * 4) + j;
                if pos < 1000 { 
                    println!("c: {}, i: {}, j: {}, pos: {}", c, i, j, pos);
                }*/
                u8_f32_arr[((flat_img.len() / 3 * c + i) * 4) + j] = u8_bytes[j]; //Write each u8_bytes position in order.
            }
        }
    }
    return u8_f32_arr; //return Vec<u8>
}

fn softmax(input: &[f32]) -> Vec<f32> {
    let max_value = input.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
    let exp_values: Vec<f32> = input.iter().map(|x| (x - max_value).exp()).collect();
    let sum: f32 = exp_values.iter().sum();

    exp_values.iter().map(|x| x / sum).collect()
}

// A wrapper for class ID and match probabilities.
#[derive(Debug, PartialEq)]
struct InferenceResult(usize, f32);
