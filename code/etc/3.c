#include <stdio.h>

//3번 문제 가위바위보
int main()
{
   int a, b;

   printf("**********가위 바위 보**********\n\n");
   printf("가위 = 0, 바위 = 1, 보 = 2\n\n");
   printf("Player1: ");
   scanf("%d", &a);
   printf("Player2: ");
   scanf("%d", &b);

   if (a == 0)
   {
      if (b == 0)   printf("Draw\n");
      else if (b == 1)   printf("Player2 Win\n");
      else if (b == 2) printf("Player1 Win\n");
      else printf("Player2 Error\n");
   }
   else if (a == 1)
   {
      if (b == 0)   printf("Player1 Win\n");
      else if (b == 1) printf("Draw");
      else if (b == 2) printf("Player2 Win\n");
      else printf("Player2 Error\n");
   }
   else if (a == 2)
   {
      if (b == 0)   printf("Player2 Win\n");
      else if(b==1) printf("Player1 Win\n");
      else if (b == 2) printf("Draw\n");
      else printf("Player2 Error\n");
   }
   else printf("Player1 Error\n");
   return 0;
}
