#define MAXSIZE 20
# include "Stack.h"


int main()
{
    Stack S;
    S.top = NULL;  

    char value[MAXSIZE] = {'\0'};
    int choice;

    while(1){
        printf("姓名: %s\t學號: %s", "尤彥", "d0001179");
        printf("\n****************************************\n");
        printf("*          (1) Insert                   *\n");
        printf("*          (2) Remove                   *\n");
        printf("*          (3) List                     *\n");
        printf("*          (4) Quit                     *\n");
        printf("*****************************************\n");
        printf("Please input one choice > ");
        scanf("%d",&choice);
        switch(choice)
        {
            case 1:
                printf("Please input one item to insert > ");
                char c;
                fflush(stdin);
                scanf(" %c",&c);
                insert(&S, &c);
                break;
            case 2:
                delete(&S, value);
                break;
            case 3:
                list(&S);
                break;
            case 4:
                exit(0);
        }
    }

    return 0;

}
