#include <stdio.h>
#include <stdlib.h>

void merge(int arr[], int p, int q, int r)
{
    int *L=NULL, *R=NULL;
    int n1=q-p+1;
    int n2=r-q;
    int i,j,k;
    
    L=(int*)malloc(n1*sizeof(int));
    R=(int*)malloc(n2*sizeof(int));
    for(i=0;i<n1;i++)
        L[i]=arr[p+i];
    for(i=0;i<n2;i++)
        R[i]=arr[q+i+1];
        
    i=j=0;
    k=p;
    while(k<=r && i<n1 && j<n2)
    {
        if(L[i]<=R[j])
            arr[k++]=L[i++];
        else
            arr[k++]=R[j++];
    }
    
    if(i<n1)
    {
        while(i<n1)
            arr[k++]=L[i++];
    }
    if(j<n2)
    {
        while(j<n2)
            arr[k++]=R[j++];
    }
    
    free(L);
    free(R);
}

void merge_sort(int arr[], int p, int r)
{
    int q=0;
    if( p<r )
    {
        q=(p+r)/2;
        merge_sort(arr, p, q);
        merge_sort(arr, q+1, r);
        merge(arr, p, q, r);
    }
}

int main(int argc, char** argv)
{
	int arr[]={3,4,2,7,0,8,6,2,4,3,6,8,2,5,9,222,34,-33,234};
	int i=0;

	merge_sort(arr,0,18);
	
	for(i=0;i<19;i++)
		printf("%d ", arr[i]);
	printf("\n");
	return 0;
}
