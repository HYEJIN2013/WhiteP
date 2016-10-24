#include <stdio.h>


//2번 문제 숫자 자릿수나누기
int main()
{
	int num;
	int a,b,c,d;

	printf("**********자릿수 나누기**********\n\n");
	printf("숫자를 입력하시오: ");
	scanf("%d",&num);
	
	a = num/1000;
	b = (num%1000)/100;
	c = (num%100)/10;
	d = num%10;

	printf("천의 자리: %d\n",a);
	printf("백의 자리: %d\n",b);
	printf("십의 자리: %d\n",c);
	printf("일의 자리: %d\n",d);
	return 0;
}
