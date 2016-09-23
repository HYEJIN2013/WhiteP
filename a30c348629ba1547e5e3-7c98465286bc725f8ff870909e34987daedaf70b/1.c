#include <stdio.h>

int main()
{
	int iSec;
	int hour, min, sec;

	printf("**********시간(초) 계산기**********\n\n");
	printf("시간(초)을 입력하시오: ");
	scanf("%d",&iSec);

	hour = iSec/3600;
	min = (iSec%3600)/60;
	sec = iSec%60;
	printf("%d초는 %d시간 %d분 %d초입니다.\n",iSec,hour,min,sec);
	return 0;
}
