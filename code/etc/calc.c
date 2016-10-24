#include <stdio.h>
#include <stdlib.h>

// 함수 선언
int addition(int,int);
int subtraction(int,int);
int multiply(int,int);
double divide(int,int);

// main()
int main()
{
	int i, m, n;

	while(1)
	{
		printf("1. 더하기 2. 빼기 3. 곱하기 4. 나누기 5. 종료: ");
		scanf("%d", &i);

		// 좋은 코드는 아님! 왜일까?
		switch(i)
		{
			case 1:
				printf("입력1: ");
				scanf("%d", &m);
				printf("입력2: ");
				scanf("%d", &n);
				printf("%d + %d = %d\n", m, n, addition(m, n));
				break;
			case 2:
				printf("입력1: ");
				scanf("%d", &m);
				printf("입력2: ");
				scanf("%d", &n);
				printf("%d - %d = %d\n", m, n, subtraction(m, n));
				break;
			case 3:
				printf("입력1: ");
				scanf("%d", &m);
				printf("입력2: ");
				scanf("%d", &n);
				printf("%d x %d = %d\n", m, n, multiply(m, n));
				break;
			case 4:
				printf("입력1: ");
				scanf("%d", &m);
				printf("입력2: ");
				scanf("%d", &n);
				printf("%d / %d = %lf\n", m, n, divide(m, n));
				break;
			case 5:
				exit(0);
				break;
			default:
				printf("1부터 5까지의 숫자를 입력하세요.\n");
				break;
		}
	}

	return 0;
}

// 함수 구현
int addition(int m, int n)
{
	return m + n;
}

int subtraction(int m, int n)
{
	return m - n;
}

int multiply(int m, int n)
{
	return m * n;
}

double divide(int m, int n)
{
	return (double)m / n;
}
