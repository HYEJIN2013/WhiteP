#include <stdio.h>
#include <stdlib.h>
#include <math.h>
 
#define SQRNUM 2 // 피제곱수
#define MAX 128 // 제곱 횟수
 
void main(void)
{
	FILE *fp1, *fp2;
	unsigned int i, j, k,
			l = 0, 
			LENGTH = 0;
	unsigned int *num;
 
	fp1 = fopen("result1.txt", "wt"); // 과정 전부 출력
	fp2 = fopen("result2.txt", "wt"); // 최종 과정만 출력
	LENGTH = MAX * log10((double)SQRNUM) + 1; // 자릿수 구하기
	num = (unsigned int*)calloc(LENGTH, sizeof(unsigned int)); 
 
	num[LENGTH - 1] = 1;
 
/* 제곱계산부분 */
	for(i = 1 ; i <= MAX ; i++)
	{
		for(j = 0 ; j < LENGTH ; j++)
		{
			if(num[j] == 0) continue; // 앞 부분의 0들은 계산 생략
			while(j < LENGTH)
			{
				num[j] = num[j] * SQRNUM;
				for(k = LENGTH - 1 ; k > 0 ; k--)
				{
					while(num[k] > 9)
					{
						num[k] = num[k] - 10;
						num[k-1] = num[k-1] + 1;
					}
				}
				j++;
			}
			break;
		}
 
/* 여기서부터 주석처리하면 result2.txt만 출력 */
		printf("%d^%d = ", SQRNUM, i); fprintf(fp1, "%d^%d = ", SQRNUM, i);
		for(j = 0 ; j < LENGTH ; j++)
		{
			if(num[j] == 0) // 앞 부분의 0들은 출력 생략
			{
				l++;
				continue;
			}
			while(j < LENGTH)
			{
				printf("%d", num[j]); fprintf(fp1, "%d", num[j]);
				if((LENGTH - 1 - j) % 3 == 0 && j < LENGTH - 1) 
				{
					printf(",");
					fprintf(fp1, ",");
				}
				j++;
			}
			break;
		}
		printf("	(%d 자리)\n", LENGTH - l); fprintf(fp1, "	(%d 자리)\n", LENGTH - l);
		l = 0;
/* 여기까지 */
	}
	
 
/* 여기서부터 주석처리하면 result1.txt만 출력 */
	fprintf(fp2, "%d^%d = ", SQRNUM, i-1);
	for(j = 0 ; j < LENGTH ; j++)
	{
		if(num[j] == 0) // 앞 부분의 0들은 출력 생략
		{
			l++;
			continue;
		}
		while(j < LENGTH)
		{
			fprintf(fp2, "%d", num[j]);
			if((LENGTH - 1 - j) % 3 == 0 && j < LENGTH - 1) fprintf(fp2, ",");
			j++;
		}
		break;
	}
	fprintf(fp2, "	(%d 자리)\n", LENGTH - l);
/* 여기까지 */
 
	fclose(fp1);
	fclose(fp2);
} 