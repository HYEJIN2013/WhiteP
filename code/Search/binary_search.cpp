#include <iostream>
#include <vector>

int binary_search(std::vector<int> *sorted_data, int value, int start_index, int end_index) {

    int mid_index = start_index + ( (end_index - start_index)/2) ;

    if( (*sorted_data)[mid_index] == value ) {
        return mid_index;
    }
    else if( start_index ==  end_index ) {
        return -1;
    }
    else {
        if( value < (*sorted_data)[mid_index] ) {
            return binary_search( sorted_data,value, start_index , mid_index );
        }
        else {
            return binary_search( sorted_data,value, mid_index , end_index );
        }
    }
}

int main() {
    std::vector<int> sorted_data(100);

    for(int i=0; i<100; ++i) {
        sorted_data[i] = i*3;
    }

    int index_of_value = binary_search(&sorted_data,33, 0, sorted_data.size()-1);

    std::cout << index_of_value <<"!" << std::endl;
    return 0;
}
