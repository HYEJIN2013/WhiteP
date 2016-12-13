#include <iostream>
using namespace std;

int main() {
	// Define a int variable
	int i = 5;
	// Declare a pointer which can point to a int
	int *i_ptr;
	// Make i_ptr point to i
	i_ptr = &i;

	cout <<"Address of i - "<<&i<<endl;
	cout <<"Address of i - "<<i_ptr<<endl;

	// A pointer is also associated with an address.
	// To get the pointer's address, use the & operator
	cout <<"Address of i_ptr - "<<&i_ptr<<endl;

	cout <<"Value of i - "<<i<<endl;
	cout <<"Value of i_ptr - "<<i_ptr<<endl;

	// We can also use the * and & operators together to get the value
	cout <<"Value of i - "<<*(&i)<<endl;

	// We can use the indirection (*) operator to get the value pointed by the pointer
	cout <<"Value of i - "<<*i_ptr<<endl;

	return 0;
}
