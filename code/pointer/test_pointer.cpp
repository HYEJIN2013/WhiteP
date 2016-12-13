#include <iostream>
#include <cstdlib>
#include <stdio.h>

using namespace std;

int main()
{
    int a=123456;
    int *aPtr = &a;

    cout<<"&a = "<<&a<<endl; // a自己的地址
    cout<<"a = "<<a<<endl;   // a所存的值
    cout<<"aPtr = "<<aPtr<<endl; // aPtr所存的值，值為a的地址
    cout<<"*aPtr = "<<*aPtr<<endl<<endl; // 值(a的地址)所對應的值(123456)

    a=a+1;
    cout<<"a = a+1"<<endl;
    cout<<"a = "<<a<<endl;
    cout<<"aPtr = "<<aPtr<<endl;
    cout<<"*aPtr = "<<*aPtr<<endl<<endl;

    cout<<"&aPtr = "<<&aPtr<<endl;  // *aPtr 自己的地址
    cout<<"*&aPtr = "<<*&aPtr<<endl;// = 自己地址裡所存的值(a的地址)
    cout<<"&*aPtr = "<<&*aPtr<<endl<<endl;    // = 值(123456)它自己的地址(a的地址)

    return 0;
}
