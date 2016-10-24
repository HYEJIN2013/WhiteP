#include <stdio.h>

int factorial(int n)
{
	if (n == 0)
		return 1;
	return n * factorial(n-1);
}

int main() {
	int number = 5;
	int result = factorial(number);
	printf("The factorial number of %i is %i!", number, result);
	return 0;
}
