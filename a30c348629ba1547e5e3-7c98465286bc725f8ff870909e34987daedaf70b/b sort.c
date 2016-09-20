#include <stdio.h> 

#define DATA 4 

int main() 

{ 

    int num[]={3,2,4,1};//초기값 

    int i, j , temp; 

     

    printf("초기 값 : "); 

    for(i=0;i<DATA;i++) 

        printf("%d ",num[i]); 

        printf("\n"); 

      

     

    for(i=0;i<DATA-1;i++)

    { 

        for(j=0;j<DATA-1;j++) 

        { 

            if(num[j] > num[j+1]) 

            { 

                temp=num[j];

                num[j]=num[j+1]; 

                num[j+1]=temp; 

            } 

        } 

    } 

 

    printf("정렬 후 : "); 

    for(i=0;i<DATA;i++) 

        printf("%d ",num[i]); 

        printf("\n"); 

     

}
