#include <stdio.h>
#include <stdlib.h>
#include <time.h>
// 숫자야구 게임.
int main(void)
{
	int e;// 게임이 다 끝난후 다시 실행할지.
	do
	{
		int Base[3], Use[3];
		int i, j, S = 0, B = 0, Ct = 0;
		int x;// 최초 실행시 게임을 실행할지.


		printf("************************************************\n");
		printf("*               숫자야구 게임                  *\n");
		printf("*                                              *\n");
		printf("*                                              *\n");
		printf("*     시작 : 1번          종료 : 0번           *\n");
		printf("************************************************\n");
		printf("    시작 하시겠습니까? : ");
		scanf("%d", &x);
		if (x == 1)
		{
			printf("숫자를 생성중 입니다.\n");
			srand(time(NULL));

			Base[0] = rand() % 9 + 1; // 1 ~ 9 값을 만들기위해 %9 + 1을 사용.
			do
			{
				Base[1] = rand() % 9 + 1; // 1번째 배열에 집어넣는다. 
			} while (Base[1] == Base[0]);

			do
			{
				Base[2] = rand() % 9 + 1; // 2번째 배열에 집어넣는다.
			} while (Base[2] == Base[0] || Base[2] == Base[1]);

			printf("숫자 생성 완료!\n");

			// 사용자의 수를 받음
			do
			{
				Ct++;
				printf("-----------%d번째 시도입니다.----------\n", Ct);

				do
				{
					printf("[1 ~ 9] 사이의 숫자 세자리를 입력하세요.\n  (수를 쓴 후 띄어쓰기 해주시고 다 쓴 후 엔터를 눌러주세요.)\n\n"); // 숫자 3개를 입력받음.
					scanf("%d", &Use[0]);
					scanf("%d", &Use[1]);
					scanf("%d", &Use[2]);

					if (Use[0] == Use[1] || Use[0] == Use[2] || Use[1] == Use[2]) // 숫자가 하나라도 중복된다면
					{
						printf("숫자가 중복되면 안됩니다.\n");
					}
					else if (Use[0] > 9 || Use[1] > 9 || Use[2] > 9) // 숫자가 하나라도 9를 넘는다면
					{
						printf("1 ~ 9 사이의 수만 입력 가능합니다. \n");
					}
				} while ((Use[0] == Use[1] || Use[0] == Use[2] || Use[1] == Use[2]) || (Use[0] > 9 || Use[1] > 9 || Use[2] > 9));
				// 조건중 하나라도 포함된다면 다시 시작.

				S = 0; // Strike
				B = 0; // Ball


				for (i = 0; i < 3; i++) // 배열의 값 비교문.
				{
					if (Use[i] == Base[i])
					{
						S++;
					}
					else if (Use[(i + 1) % 3] == Base[i]) // 2번째 배열의 값을 비교.
					{
						B++;
					}
					else if (Use[(i + 2) % 3] == Base[i]) // 1번째 배열의 값을 비교.
					{
						B++;
					}

				}


				printf("\n");
				printf("%d Strike, %d Ball\n", S, B); // Strike와 Ball을 출력.

				if (S < 3)
				{
					printf("다시 숫자를 정하세요!\n");
				}

			} while (S < 3); // S가 3이 아니라면 다시 반복.

			printf("******************\n");
			printf("*     정답!!     *\n");
			printf("*    %d번만에    *\n", Ct);
			printf("*     성공!!     *\n");
			printf("******************\n");

			printf("계속 하려면 ""1"", 종료하려면 ""아무키""나 누르세요\n");
			scanf("%d", &e);
		}
		if (x != 1 || e != 1)
			break;
	} while (e == 1);


	system("pause");
	return 0;
}
