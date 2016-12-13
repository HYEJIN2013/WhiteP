When you have a pointer pointing to some memory there are three different things you must understand:
- there is "what is pointed" by the pointer (the memory)
- this memory address
- not all pointers need to have their memory deleted: you only need to delete memory that was dynamically allocated (used new operator).

Imagine:

int *ptr = new int; 
// ptr has the address of the memory.
// at this point, the actual memory doesn't have anything.
*ptr = 8;
// you're assigning the integer 8 into that memory.
delete ptr;
// you are only deleting the memory.
// at this point the pointer still has the same memory address (as you could
//   notice from your 2nd test) but what inside that memory is gone!
When you did

ptr = NULL;
// you didn't delete the memory
// you're only saying that this pointer is now pointing to "nowhere".
// the memory that was pointed by this pointer is now lost.
C++ allows that you try to delete a pointer that points to null but it doesn't actually do anything, just doesn't give any error.
