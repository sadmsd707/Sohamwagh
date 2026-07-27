#include <stdio.h>
int length(char[]);
void reverse(char[]);
int main() {
    char str[50];
    printf("Enter a String: ");
    scanf("%s", str);
    reverse(str);
    return 0;
}
int length(char a[]) {
    int len = 0;
    while (a[len] != '\0') {
        len++;
    }
    return len;
}
void reverse(char a[]) {
    int al = length(a);
    int i;
    char temp;
    for (i = 0; i < al / 2; i++) {
        temp = a[i];
        a[i] = a[al - 1 - i];
        a[al - 1 - i] = temp;
    }
    printf("Reversed String: %s", a);
}
