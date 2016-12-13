#include <iostream> /// std::cout; std::endl;
#include <string> /// std::string;

bool lengthCompare (const std::string &cs1, const std::string &cs2) /// just compares some strings
{
    if (cs1.size() > cs2.size())
        return true;
    else
        return false;
}

bool (*pf) (const std::string &, const std::string &); /// points to lengthCompare ();

int main()
{
    bool b1 = false, b2 = false, b3 = false;

    pf = &lengthCompare; /// or lengthCompare; --> gets the address of lengthCompare;

    b1 = pf ("hello", "goodbye");
    b2 = (*pf)("hello", "goodbye");
    b3 = lengthCompare ("hello", "goodbye");


    std::cout << b1 << " " << b2 << " " << b3
              << std::endl;

    return 0;
}
