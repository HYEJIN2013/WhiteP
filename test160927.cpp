// test160927.cpp : 콘솔 응용 프로그램에 대한 진입점을 정의합니다.
//

#include "stdafx.h"
#include "stdlib.h"
#define N 1000

int main()
{
	char s[N], i = 0;
	scanf("%c", &s[0]);
	while (s[i] != '\n')
		scanf("%c", &s[++i]);
	for (int j = i - 1; j >= 0; j--)
		printf("%c", s[j]);


    return 0;
}

