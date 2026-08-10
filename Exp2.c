#include <stdio.h>
int binarySearch(int arr[], int low, int high, int key) {
    if (low > high)
        return -1;
int mid = low + (high - low) / 2;
    if (arr[mid] == key)
        return mid;
    if (key < arr[mid])
        return binarySearch(arr, low, mid - 1, key);
    return binarySearch(arr, mid + 1, high, key);
}

int main() {
    int arr[100], n, key, result;

    printf("Enter number of elements (sorted order): ");
    scanf("%d", &n);

    printf("Enter %d sorted integers:\n", n);
    for (int i = 0; i < n; i++)
        scanf("%d", &arr[i]);

    printf("Enter the element to search: ");
    scanf("%d", &key);

    result = binarySearch(arr, 0, n - 1, key);

    if (result != -1)
        printf("Element found at index %d\n", result);
    else
        printf("Element not found\n");

    return 0;
}
