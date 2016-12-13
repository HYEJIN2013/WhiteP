// xcode
// paulogp
#include <iostream>

using namespace std;

int main (int argc, const char * argv[])
{
    // initialize
    int the_value = 500;
    int *the_pointer = NULL;

    // point to the_value
    the_pointer = &the_value;

    // output
    cout << "value " << *the_pointer << " stored at " << the_pointer << endl;;

    return 0;
}
