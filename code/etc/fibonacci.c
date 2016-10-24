#include <stdio.h>

int fibonacci(int);

int main()
{
	int i, n;

	printf("n: ");
	scanf("%d", &n);

	for(i = 0; i < n; i++)
	{
		printf("%d ", fibonacci(i));
	}

	return 0;
}

int fibonacci(int n)
{
	// F(0) = 0 and F(1) = 1
	// 재귀 함수가 끝나는 종료조건
	if(n == 0 || n == 1)
		return n;
	// F(n) = F(n-1) + F(n-2)
	// 재귀 함수에서 재귀되는 부분
	else
		return fibonacci(n-1) + fibonacci(n-2);
	
	/* one line */
	// return (n == 0 || n == 1) ? n : fibonacci(n-1) + fibonacci(n-2);
}
