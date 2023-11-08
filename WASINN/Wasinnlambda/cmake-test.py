import cmake

# Set the source directory
source_directory='/tmp/wasinn'

# Set the build directory
build_directory='/tmp/wasinn/build'

# Set CMake variables
cmake_variables = {
    'CMAKE_BUILD_TYPE': 'Release',
    'WASMEDGE_PLUGIN_WASI_NN_BACKEND': 'PyTorch'
}

# Configure and build the project
cmake.build(source_directory, build_directory, variables=cmake_variables)

# # Install the project
# cmake.build(build_directory, target='install')
