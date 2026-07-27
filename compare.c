#include <stdio.h>

void compare(char[], char[]);

int i;

int main() {
    char str1[50], str2[50];

    printf("Enter First String: ");
    scanf("%s", str1);

    printf("Enter Second String: ");
    scanf("%s", str2);

    compare(str1, str2);

    return 0;
}

void compare(char str1[50], char str2[50]) {
    i = 0;

    while (str1[i] != '\0' && str2[i] != '\0') {
        if (str1[i] != str2[i]) {
            break;
        }
        i++;
    }

    if (str1[i] == str2[i]) {
        printf("Both Strings are Equal\n");
    }
    else if (str1[i] > str2[i]) {
        printf("First String is Greater than Second String\n");
    }
    else {
        printf("First String is Smaller than Second String\n");
    }

   
}
