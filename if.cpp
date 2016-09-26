#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;

    if (a < b) {
        cout << "작다" << endl;
    }

    if (a > b) {
        cout << "크다" << endl;
    }

    if (a == b) {
        cout << "같다" << endl;
    } else {
        cout << "같지 않다" << endl;
    }

    return 0;
}
