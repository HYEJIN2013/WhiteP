#include <iostream>

using namespace std;

// =============== smart pointer for int ==============================

class smtptr {
  int *ref;
  int *count;
public:
  smtptr(int *p) {
    if(!p) return;
    ref = p;
    count = new int;  // gist
    *count = 1;
  }
  
  smtptr(smtptr &p) {
    ref = p.ref;
    count = p.count;
    (*count)++;    // gist
  }
  
  smpptr& operator = (smtptr &p) {
    if( *count > 0) remove_one_ref();
    if(this == &p) return *this;  // gist
    ref = p.ref;
    count = p.count;
    (*count)++;
    return *this;  // gist!
  }
  
  int& operator * () { return *ref; }
  int* operator -> () { return ref; }
  
protected:
  void remove_one_ref() {
    (*count)--;
    if(*count == 0) {
      delete ref;
      ref = NULL; // gist
      delete count;
      count = NULL; // gist
    }
  }
};

// ===================== generic smart pointer ========================
template<class T> 
class sun_ptr {
	T *ref;
	int *count;
public:
	sun_ptr(T *ptr) {
		ref = ptr;
		count = new int;
		*count = 1;
	}
	sun_ptr(sun_ptr<T> &ptr) {
		ref = ptr.ref;
		count = ptr.count;
		(*count)++;
	}

	~sun_ptr() { remove_one_ref(); }
	sun_ptr<T>& operator=(sun_ptr<T> &ptr) {
		if( *count > 0)
			remove_one_ref();
		if(this == &ptr) return *this;
		else {
			ref = ptr.ref;
			count = ptr.count;
			(*count)++;
			return *this;
		}
	}
	T& operator*() { return *ref; }
	T* operator->() { return ref; }
	T getCount() {
		return *count;
	}
protected:
	void remove_one_ref() {
		(*count)--;
		if(*count == 0) {
			delete ref;
			ref = NULL;
			delete count;
			count = NULL;
		}
	}
};




int main()
{
    int *p = new int(99);
    sun_ptr<int> ptr(p);
    sun_ptr<int> ptr2 = ptr;
    sun_ptr<int> ptr3 = ptr;
    cout << ptr.getCount() << endl;
    cout << *ptr;
    return 0;
}
