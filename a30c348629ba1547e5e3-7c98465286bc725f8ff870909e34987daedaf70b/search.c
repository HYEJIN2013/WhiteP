#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#define bitlen24 (int)(pow(2,24)-1)

int laddr[64];
int delai=0;
int withdraw[64];
int searchaddr=0;
int transcnt1=0;
int transcnt2=0;

int comparelong(void)
{
    int myloop;
    int comval=searchaddr;

    transcnt1++;
    transcnt2++;

    for(myloop=0;myloop<64;myloop++)
    {
        if((laddr[myloop]<=comval)&&withdraw[myloop]==0)return(1);
    }
    return(0);
}

void setwithdraw(int inval)
{
    int myloop;

    transcnt1++;
    transcnt2++;

    for(myloop=0;myloop<64;myloop++)
    {
        if(laddr[myloop]==inval)
        {
            withdraw[myloop]=1;
            //return;
        }
    }
}


void setsearch(int inval,int shift)
{

    transcnt1++;
    transcnt2++;

    inval&=0xFF;
    searchaddr&=0xFF00FFFF;
    searchaddr|=inval<<16;
}

void setsearch_h(int inval)
{

    transcnt1++;
    transcnt2++;

    inval&=0xFF;
    searchaddr&=0xFF00FFFF;
    searchaddr|=inval<<16;
}

void setsearch_m(int inval)
{
    transcnt1++;
    transcnt2++;

    inval&=0xFF;
    searchaddr&=0xFFFF00FF;
    searchaddr|=inval<<8;
}

void setsearch_l(int inval)
{
    transcnt1++;
    transcnt2++;

    inval&=0xFF;
    searchaddr&=0xFFFFFF00;
    searchaddr|=inval;
}

void bin(int n)
{
 /* step 1 */
 if (n > 1)
     bin(n/2);
 /* step 2 */
 printf("%d", n % 2);
}

int main()
{
    int cing=0;
    int foundcount=0;
    int prevaddr=0;
    int bitsearchcount=0;
    int max;
    srand(time(NULL));
    printf("Hello ! please enter your random number range( 6-24 )\n");
    while(1){
        scanf("%d",&max);
        if(max >= 6 && max <=24) break ;
        printf("again please.\n");
    }
    for(delai=0;delai<64;delai++){
        laddr[delai] = rand()%(int)(pow(2,max));
        printf("%6d ", laddr[delai]);
        withdraw[delai]=0;
    }
    printf("\nlet's start!\n");
    cing=0xFFFFFF;
    bitsearchcount=0;
    delai = 0;
    setsearch_l((cing)&0xFF);
    setsearch_m((cing>>8)&0xFF);
    setsearch_h((cing>>16)&0xFF);
    bitsearchcount=23;
    while(bitsearchcount>=0){
        cing&=~(1<<bitsearchcount);
        if(bitsearchcount>15){
            setsearch_h((cing>>16)&0xFF);
        } else if(bitsearchcount>7){
            setsearch_m((cing>>8)&0xFF);
        } else{
            setsearch_l((cing)&0xFF);
        }
        if(comparelong()==0)
        {
            cing|=(1<<bitsearchcount);
            if(bitsearchcount==16)setsearch_h((cing>>16)&0xFF);
            if(bitsearchcount==8)setsearch_m((cing>>8)&0xFF);
        }
        bitsearchcount--;
    }
    setwithdraw(cing);
    printf("searchcount=%d,longaddr=%d,trans1=%d,trans2=%d\n",delai,cing,transcnt1,transcnt2);
    transcnt1=0;
    delai++;
    cing++;
    bitsearchcount = 0 ;
    int validBit = 0;
    bitsearchcount = validBit ;
    while(bitsearchcount < 24){
        if(bitsearchcount>15) setsearch_h((cing>>16)&0xFF);
        else if(bitsearchcount>7) setsearch_m((cing>>8)&0xFF);
        else setsearch_l((cing)&0xFF);
        if(comparelong()==0){ // nobody lower than the address
            while((cing >> bitsearchcount)&0x01)bitsearchcount++;
            // bin(cing);
            // printf("  cinn = 0x%d , bitsearchcount = %d \n", cing , bitsearchcount);
            cing|=(1<<bitsearchcount);
        }else{  // some addresses are in this range
            // bin(cing);
            // printf("  cinn = 0x%d , bitsearchcount = %d \n", cing , bitsearchcount);
            cing|=(1<<bitsearchcount);
            bitsearchcount--;
            printf("diff = %d bit \n", bitsearchcount);
            while(bitsearchcount>=0){
                cing&=~(1<<bitsearchcount);
                // printf("      ");
                // bin(cing);
                // printf("  %d \n", cing);
                if(bitsearchcount>15){
                    setsearch_h((cing>>16)&0xFF);
                } else if(bitsearchcount>7){
                    setsearch_m((cing>>8)&0xFF);
                } else{
                    setsearch_l((cing)&0xFF);
                }
                if(comparelong()==0)
                {
                    cing|=(1<<bitsearchcount);
                    if(bitsearchcount==16)setsearch_h((cing>>16)&0xFF);
                    if(bitsearchcount==8)setsearch_m((cing>>8)&0xFF);
                }
                bitsearchcount--;
            }
            setwithdraw(cing);
            printf("searchcount=%d,longaddr=%d,trans1=%d,trans2=%d\n",delai,cing,transcnt1,transcnt2);
            delai++;
            transcnt1=0;
            bitsearchcount = 0;
        }
    }    
    printf("done\n");
    return 0;
}
