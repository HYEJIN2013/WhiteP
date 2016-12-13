#include <iostream>
using namespace std;

/* prototype */
void show( double **A );
void add( double **A, double **B, double **C );




int main(int argc, char const *argv[])
{
	int n;
	cin >> n;

	double **A = new double *[n];
	double **B = new double *[n];	
	for (int i = 0; i < n; ++i)
	{
		A[i] = new double[n];
		B[i] = new double[n];
	}

	int num = 0;
	for (int i = 0; i < n; ++i)
	{
		for (int x = 0; x < n; ++x)
		{
			/* get number to add */
			cout << "insert [" << i << ',' << x << "]  "; 
			cin >> num;
			/* assign to matrix */
			A[i][x] = num;
		}
	}

	show( A );


	cout << endl << endl;
	return 0;
}



void add( double **A, double **B, double **C )
{

}

//void sum()
void show( double **A )
{
	int n = sizeof(A) / 2;
	for (int i = 0; i < n; ++i)
	{
		cout << endl << '\t';
		for (int x = 0; x < n; ++x)
		{
			cout << A[i][x] << ( A[i][x] < 10 ? "  " : " ");
		}
	}
}
