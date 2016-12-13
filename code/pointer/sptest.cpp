#include "sptest.h"
#include <stdio.h>

class test {
public:
	test() {
		printf("Test constructor\n");
		field = new char[20];
		is_deleted = false;
	}
	~test() {
		printf("Test destructor\n");
		if (!is_deleted) // If you see the warning, something goes wrong
			printf("Test was not cleaned up properly!\n");
		delete field;
	}
	void hello() {
		printf("Hello, test\n");
	}
	void del() {
		is_deleted = true;
	}
	char *field;
	bool is_deleted;
};

typedef Csptr<test> sp_test;
template <> void Csptr<test>::Cwrap::Cleanup() {
	if (!m_value)
		return;
	m_value->del();
	delete m_value;
}

// Typedef and cleanup using a macro. Should be expanded like this:
//	typedef Csptr<int> spint;
//	template <> void Csptr<int>::Cwrap::Cleanup() {
//	// Nothing to do
//		printf("Int smartptr cleanup!\n");
//	}
SMARTPTR_CLEANUP_BEGIN(spint, int)
// Nothing to do
	printf("Int smartptr cleanup!\n");
SMARTPTR_CLEANUP_END

template <> bool Csptr<int>::IsValid() {
	printf("Something checks if the pointer is valid at all\n");
	return m_wrap != NULL;
}

test *make_test() {
	return new test();
}

sp_test make_sptest() {
	return sp_test(*make_test());
}

int a = 15;

int main(int argc, char *argv[]) {
	sp_test spt(*make_test());
	Csptr<test> spt2;   // Same as "sp_test spt2;"
	sp_test spt3(make_sptest());
	Csptr<int> spint, spint2(a);
//	Csptr<char> spchar; // Won't compile since there's no cleanup for char defined
	spt->hello();
	spt2->hello();
	spt3->hello();

	printf("spt is %svalid\n", spt.IsValid() ? "" : "in");
	printf("spt2 is %svalid\n", spt2.IsValid() ? "" : "in");
	printf("spint is %svalid\n", spint.IsValid() ? "" : "in");
	printf("spint2 is %svalid\n", spint2.IsValid() ? "" : "in");

	spt3 = NULL;
	spt3 = spt;
	spt3.Unlink();

	spt2 = spt;
	spt2->hello();

	printf("woof\n");
	return 0;
}
