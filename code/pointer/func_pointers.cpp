#include <iostream>
#include <cstdlib>
#include <cstring>
using namespace std;

int main() {
	// Integer elements to be sorted
	int i_arr[] = {5, 20, 3, 96, 37, 12, 2, 56, 39};

	// Integer comparison function prototype
	int int_comparison_function(const void *, const void *);

	// qsort routine - with an integer comparison function
	qsort(i_arr, sizeof(i_arr)/sizeof(int), sizeof(int), int_comparison_function);

	// Print out the sorted integers
	for (size_t i = 0; i < sizeof(i_arr)/sizeof(int); ++i)
		cout <<i_arr[i]<<"\t";

	cout <<endl;

	// Strings to be sorted
	char *s_arr[] = {"Hello", "Bye", "Morning", "World", "English", "An", "Black", "Fox"};

	// String comparison function prototype
	int str_comparison_function(const void *, const void *);

	// qsort routine - with an string comparison routine
	qsort(s_arr, sizeof(s_arr)/sizeof(char *), sizeof(char *), str_comparison_function);

	// Print out the sorted strings
	for (size_t i = 0; i < sizeof(s_arr)/sizeof(char *); ++i)
		cout <<s_arr[i]<<"\t";

	return 0;
}

// Comparison function for pointers
int int_comparison_function(const void *num1, const void * num2)
{
	return ( *(int*)num1 - *(int*)num2 );
}

// Comparison function for strings
int str_comparison_function(const void *str1, const void *str2)
{
	return strcmp(*(char **)str1, *(char **)str2);
}
