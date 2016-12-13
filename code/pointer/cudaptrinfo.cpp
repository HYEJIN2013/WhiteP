#include <cuda_runtime.h>
#include <iostream>

void print_ptr_attr( const cudaPointerAttributes& pa ) {
    std::cout << "Pointer attributes:\n";
    std::string mt = pa.memoryType == cudaMemoryTypeHost ? "cudaMemoryTypeHost"
                                                         : "cudaMemoryTypeDevice";
    std::cout << "  memoryType:    " << mt << std::endl;
    std::cout << "  device:        " << std::hex << pa.device << std::endl;
    std::cout << "  devicePointer: " << std::hex << pa.devicePointer << std::endl;
    std::cout << "  hostPointer:   " << pa.hostPointer << std::endl;
}

int main( int argc, char** argv ) {
    char* dev = 0;
    char* host = 0;
    cudaMalloc( &dev, 0x10000 );
    host = new char[ 0x10000 ];
    std::cout << std::endl;
    std::cout << "Device pointer info" << std::endl
              << "-------------------" << std::endl;
    cudaPointerAttributes attr;
    cudaPointerGetAttributes( &attr, dev );
    print_ptr_attr( attr );
    std::cout << std::endl;
    std::cout << "Host pointer info" << std::endl
              << "-----------------" << std::endl;
    cudaPointerAttributes attr2;
    cudaPointerGetAttributes( &attr2, host );
    print_ptr_attr( attr2 );

    cudaFree( dev );
    delete [] host;

    return 0;
}
