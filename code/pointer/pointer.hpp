#define Pointer(T) T *
#define ImmutableValuePointer(T) const T *
#define ImmutableAddressPointer(T) T * const
#define ImmutablePointer(T) const T * const

template <typename T>
class Pointer {
public:
	typedef T *type;
	typedef const T * immutableValue;
	typedef T * const immutableAddress;
	typedef const T * const immutableAll;
};
