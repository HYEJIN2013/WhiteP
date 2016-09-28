stringreverse.c
/*stringreverse*/
 #include<stdio.h>
#include<string.h>
void main()
{
    char str[50];
    char rev;
    printf("Enter any string : ");
    scanf("%s",str);
    rev = strrev(str);
   
    printf("Reverse string is : %s",rev);
   
    return 0;
}