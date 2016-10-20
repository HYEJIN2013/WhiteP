#include"sort.h" 
20 #include"cuda_sort.h" 
21 #include<string.h> 
22 #include<stdlib.h> 
23 
 
24 clock_t start, end; 
25 double elapsed_time; 
26 int numberOfComparisons; 
27 int numberOfSwaps; 
28 
 
29 
 
30 void selection_sort(int *array, int size){ 
31     int i, j, min, aux; 
32       for (i = 0; i < (size-1); i++){ 
33         min = i; 
34         for (j = (i+1); j < size; j++) { 
35             numberOfComparisons++; 
36             if(array[j] < array[min]){ 
37                 min = j; 
38               } 
39         } 
40         if (i != min){ 
41             aux = array[i]; 
42               array[i] = array[min]; 
43               array[min] = aux; 
44               numberOfSwaps++; 
45         } 
46     } 
47 } 
48 
 
49 
 
50 void insertion_sort(int *array, int size) { 
51    int i, j, selected; 
52    for (i = 1; i < size; i++){ 
53       selected = array[i]; 
54       j = i - 1; 
55       while ((j >= 0) && (selected < array[j])) { 
56          array[j+1] = array[j]; 
57          j--; 
58          numberOfComparisons++; 
59       } 
60       numberOfSwaps++; 
61       array[j+1] = selected; 
62    } 
63 } 
64 
 
65 void shell_sort(int *array, int size) { 
66     int i , j , value; 
67     int gap = 1; 
68     while(gap < size) { 
69         gap = 3*gap+1; 
70     } 
71     while (gap > 1) { 
72         gap /= 3; 
73         for(i = gap; i < size; i++) { 
74             value = array[i]; 
75             j = i - gap; 
76             while (j >= 0 && value < array[j]) { 
77                 array [j + gap] = array[j]; 
78                 j -= gap; 
79                 numberOfComparisons++; 
80                 numberOfSwaps++; 
81             } 
82             array [j + gap] = value; 
83         } 
84     } 
85 } 
86 
 
87 void quick_sort(int array[], int left, int right) { 
88     int i, j, pivot, y; 
89     i = left; 
90     j = right; 
