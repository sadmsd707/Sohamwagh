#include <stdio.h>

int arr[5];
int flag = 0;

void search(int target) {
    for (int i = 0; i < 5; i++) {
       
        if (arr[i] == target) {
            flag = 1;
            break;
        }
    }
}

int main() {
    int target;
    
    printf("Enter 5 integers:\n");
    for (int i = 0; i < 5; i++) {
        scanf("%d", &arr[i]);
    }
    
    printf("Entered arr: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    
    printf("Enter the target number:\n");
    scanf("%d", &target);
    
    search(target);
    
   
    if (flag == 1) {
        printf("The number is found.\n");
    } else {
        printf("The number is not found.\n");
    }
    
    return 0;
}
