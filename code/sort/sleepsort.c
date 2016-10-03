#include<stdio.h>
#include<pthread.h>

void * createThread(void * a)
{  	
	int *temp = (int *) a;
	int b = *temp;
	sleep(b);
	printf("%d  ",b);
}
 
int main()
{
	int array[5]={4,15,7,2,5};
	int i;

	pthread_t thread[5];
	
  	for(i=0;i<5;i++)
  		pthread_create(&thread[i],NULL,createThread,&array[i]);	
		
	for(i=0;i<5;i++)
		pthread_join(thread[i],NULL);
	
	return 0;
}
  
