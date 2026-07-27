#include <stdio.h>
int length(char[]);
void palindrom(char[]);
int main() {
    char str[50];
    printf("Enter a String: ");
    scanf("%s", str);
    palindrom(str);
    return 0;
}
int length(char a[]) {
    int len = 0;
    while (a[len] != '\0') {
        len++;
    }
    return len;
}
void palindrom(char a[]) {
    int l = length(a);
    int flag = 0;
    int i;
    for (i = 0; i < l / 2; i++) {
        if (a[i] != a[l - 1 - i]) {
            flag = 1;
            break;
        }
    }
    if (flag == 0)
        printf("The String is Palindrome");
    else
        printf("The String is Not Palindrome");
}
