1 #include <stdio.h> 
2 #include <stdlib.h> 
3 #include <string.h> 
4 #include <time.h> 
5 #include <unistd.h> 
6 
 
7 void shuffle(int *array, size_t n); 
8 void print_array(int *my_array, int array_size); 
9 
 
10 int main(int argc, char *argv[]){ 
11 
 
12   int array_create_size = atoi(argv[1]); 
13 
 
14   if (array_create_size < 1){ 
15     printf("Input must be a positive integer !\n"); 
16     return 1; 
17   } 
18   // Genereate the array 
19   int my_array[array_create_size]; 
20   for (int i = 0; i <= array_create_size; i++){ 
21     my_array[i] = i; 
22   } 
23 
 
24   // Print my array 
25   print_array(my_array, array_create_size); 
26 
 
27   printf("Suffeled Array: \n"); 
28 
 
29   // Shuffle the array and print it 
30   shuffle(my_array, array_create_size);  
31   print_array(my_array, array_create_size); 
32 
 
33 
 
34 
 
35   // Now lets try to sort using bubble 
36 
 
37   printf("Now, let sort the array using bubble sort\n"); 
38   sleep(1); 
39 
 
40   int sorted = 1; 
41 
 
42   while (sorted == 1){ 
43     for (int i = 0; i <= array_create_size; i++){ 
44       if (i + 1 <= array_create_size ){ 
45         if (my_array[i] > my_array[i+1]){ 
46           int a = my_array[i]; 
47           int b = my_array[i+1]; 
48           // switch 
49           my_array[i] = b; 
50           my_array[i+1] = a; 
51           //sorted = 0; 
52         } 
53         else{ 
54           //sorted = 1; 
55         } 
56       } 
57       usleep(20000); 
58       printf("Sorting: \n"); 
59       print_array(my_array, array_create_size); 
60     } 
61   } 
62 
 
63 } 
64 
 
65 void print_array(int *my_array, int array_size){ 
66 
 
67   printf("["); 
68   for (int i = 0; i <= array_size; i++){ 
69     printf("%d, ", my_array[i]); 
70   } 
71   printf("]\n"); 
72 
 
73 } 
74 
 
75 
 
76 void shuffle(int *array, size_t n) { 
77     struct timeval tv; 
78     gettimeofday(&tv, NULL); 
79     int usec = tv.tv_usec; 
80     srand48(usec); 
81 
 
82 
 
83     if (n > 1) { 
84         size_t i; 
85         for (i = n - 1; i > 0; i--) { 
86             size_t j = (unsigned int) (drand48()*(i+1)); 
87             int t = array[j]; 
88             array[j] = array[i]; 
89             array[i] = t; 
90         } 
91     } 
92 } 
