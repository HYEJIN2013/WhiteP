#include <iostream>
#include <boost/shared_ptr.hpp>

using namespace std;
using namespace boost;

class TestClass {
public:
    TestClass (int value) : testValue(value) { cout << "TestClass constructor" << endl; };
    virtual ~TestClass () { cout << "TestClass destructor" << endl;};

private:
    int testValue;

    //getters and setters
    public: int getTestValue(){ return testValue; }
    public: void setTestValue(int testValue){ this->testValue = testValue;}
};

/* ======= Function ==================================================
 *   Name: main
 *   Description: main entry Function
 * =================================================================== 
 */
int main(int argc, const char **argv)
{
    //I - initialization of shared pointer
    boost::shared_ptr<TestClass> intPointer(new TestClass(5));
    boost::shared_ptr<TestClass> intPointer2(new TestClass(6));

    //II - printing values of pointers
    cout << "*intPointer: " << (*intPointer).getTestValue() << endl;
    cout << "*intPointer2: " << (*intPointer2).getTestValue() << endl;

    //III - set two pointers having ownership to the same resource (impossible
    //for scoped_ptr). Here value which intPointer points to will be destructed and its 
    //intPointer starts to points to the same value as intPointer2
    intPointer = intPointer2;

    //IV- print values after change ownership
    cout << "*intPointer: " << (*intPointer).getTestValue() << endl;
    cout << "*intPointer2: " << (*intPointer2).getTestValue() << endl;

    return 0;
}
