bool binarySearch(int key, int values[], int n)
{
    int min = 0;
    int max = n - 1;
    
    // run code while the min/max are still present
    while (min <= max)
    {
        // find the midpoint
        int mid = (min + max) / 2;
        
        // if he midpoint equals key, then return true
        if (values[mid] == key)
        {
            return true;
        }
        
        // if mid is in the upper bound, change min to the midpoint
        else if (values[mid] < key)
        {
            min = mid + 1;
        }
        
        // if key is in lower bound, change max to the midpoint
        else if (values[mid] > key)
        {
            max = mid - 1;
        }
    }
    // if key was not present, return false
    return false;
}
