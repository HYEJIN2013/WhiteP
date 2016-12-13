#include <cctype>
#include <iostream>
#include <string>

using namespace std;

// transform upper or lower
void string_transform(string *str)  // get address
{
    for (int i = 0; i < (*str).length(); i++)  // scan string from begin to end
    {
        if((*str)[i] >= 'a' && (*str)[i] <= 'z') // means a~z
            (*str)[i] = toupper( (int)((*str)[i]) );      // is the same as below
            //(*str)[i] += 'A' - 'a';
            
        else if((*str)[i] >= 'A' && (*str)[i] <= 'Z') // means A~Z
            (*str)[i] = tolower( (int)((*str)[i]) );  // is the same as below
            //(*str)[i] += 'a' - 'A';
    }
}

int main()
{
    string str1;
    cin >> str1;

    //****************** Solution 1 ******************
    string *ptr = &str1;    // put str1's address to pointer ptr
    string_transform(ptr); // input address to "string_transform"

    /* NOTICE
    string *ptr = &str1;  is the same as below
    string *ptr;
    ptr = &str1;
    */
    //************************************************


    //****************** Solution 2 ******************
    // string_transform(&str1); // input str1's address to "string_transform" directly
    //************************************************

    cout << str1 << endl;   // 請想想為何使用 Solution 1, str1 也會被更動?

    return 0;
}
