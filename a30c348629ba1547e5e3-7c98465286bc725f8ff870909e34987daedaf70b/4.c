#include <stdio.h>

int main()
{
	char alpha;
	printf("**********대소문자전환**********\n\n");
	printf("알파벳을 입력하시오: ");
	scanf("%c",&alpha);
	if(65 <= alpha && alpha <91)
	{
		printf("%c -> %c\n",alpha, alpha+32);
	}
	else if(97 <= alpha && alpha < 123)
	{
		printf("%c -> %c\n",alpha, alpha -32);
	}
	else
	{
		printf("잘못된 입력이거나 알파벳이 아닙니다.\n");
	}
	return 0;
}
