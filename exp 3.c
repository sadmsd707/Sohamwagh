#include <stdio.h>
#include <stdbool.h>

void bubbleSort(int arr[], int n) {
    int temp;
    bool swapped;
   
    for (int i = 0; i < n - 1; i++) {
        swapped = false;
      
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                
                swapped = true; 
            }
        }
        
        if (!swapped) {
            break;
        }
    }
}

void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int n;

    printf("Enter the number of elements: ");
    if (scanf("%d", &n) != 1 || n <= 0) {
        printf("Invalid array size.\n");
        return 1;
    }

    int data[n];

    printf("Enter %d integers:\n", n);
    for (int i = 0; i < n; i++) {
        printf("Element %d: ", i + 1);
        scanf("%d", &data[i]);
    }
    
    printf("\nOriginal array: \n");
    printArray(data, n);
    
    bubbleSort(data, n);
    
    printf("Sorted array in ascending order: \n");
    printArray(data, n);
    
    return 0;
}

