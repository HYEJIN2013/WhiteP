#include <iostream>
using namespace std;

int main() {

	int i_arr[2][2][2] = {
			{
					{1, 2},
					{3, 4}
			},
			{
					{5, 6},
					{7, 8}
			}
	};

	cout <<i_arr<<"\t"<<*i_arr<<"\t"<<**i_arr<<endl;
	cout <<i_arr+1<<endl;
	cout <<*i_arr+1<<endl;
	cout <<**i_arr+1<<endl;
	cout <<***i_arr+1<<endl;
	return 0;
}
