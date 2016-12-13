#include <iostream>
using namespace std;

int main() {
	int i = 5;
	int *i_ptr = &i;

	// A pointer to pointer is declared as below
	int **i_ptr_ptr;

	// It can be made to point to a pointer using & operator
	i_ptr_ptr = &i_ptr;

	// When de-referencing, we need to rightly use the number of de-referencing(*) operators
	// Since it is a pointer to a pointer, we have to use 2
	// Every other expressions remain the same0
	cout <<"Address of i - "<<&i<<endl;
	cout <<"Value of i - "<<**i_ptr_ptr<<endl;

	// Other expressions
	cout <<"Address of first level pointer - "<<&i_ptr<<endl;
	cout <<"Address of first level pointer - "<<i_ptr_ptr<<endl;

	cout <<"Address of pointer to a pointer - "<<&i_ptr_ptr<<endl;
	cout <<"Value of pointer to a pointer - "<<i_ptr_ptr<<endl;

	// Function prototype
	void print();
	// The below declaration is a pointer to a function with no parameters and returns nothing
	void (*func_ptr_print)();

	// Make the function pointer to point to a function
	func_ptr_print = print;

	// Invoke print() using the function pointer
	(*func_ptr_print)();

	return 0;
}

void print() {
	cout <<"Hello World"<<endl;
}
