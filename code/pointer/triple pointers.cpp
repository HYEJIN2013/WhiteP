#include <iostream>

using namespace std;

int main()
{
   cout << "Hello World" << endl; 
   int*** a;
   a = new int**[10];
   for (int i = 0; i < 10; i++) {
       a[i] = new int*[10];
       for (int j =0; j < 10; j++) {
           a[i][j] = new int[10];
       }
   }
   
   for (int i = 0; i < 10; i++)
       for (int j =0; j < 10; j++)
           for (int k = 0; k < 10; k++)
                a[i][j][k] = i*10 + j*10 + k;
                
   for (int i = 0; i < 10; i++) {
       for (int j =0; j < 10; j++){
           for (int k = 0; k < 10; k++)
                cout << a[i][j][k] << "\t";
            cout << endl;
       }
       cout << endl;
    }
   
   return 0;
}
