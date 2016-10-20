#include <iostream>
#include <vector>

using namespace std;

template <typename t>
typename vector<t>::iterator mbsearch(vector<t> &haystack, t key)
{
    typename vector<t>::iterator left, middle, right;
    left = haystack.begin();
    right = haystack.end();

    while (left <= right) {
        middle = left + (right - left) / 2;
        if (*middle == key) {
            return middle;
        } else if (*middle < key) {
            left = middle + 1;
        } else {
            right = middle - 1;
        }   
    }   

    return haystack.end();
}

int main()
{
    int arr[] = {1, 2, 3, 4, 5, 6, 7, 8, 9}; 
    vector<int> vi(arr, arr+9);

    vector<int>::iterator pos = mbsearch(vi, 6); 
    if (pos != vi.end()) {
        cout << "find:" << *pos << endl;
    } else {
        cout << "not find." << endl;
    }   

    return 0;
}
