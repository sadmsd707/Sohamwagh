#include <stdio.h>
int length(char[]);
void copy(char[], char[]);
int main() {
    char str1[50], str2[50];
    printf("Enter Source String: ");
    scanf("%s", str2);
    copy(str1, str2);
    return 0;
}

int length(char a[]) {
    int len = 0;
    while (a[len] != '\0') {
        len++;
    }
    return len;
}
void copy(char a[], char b[]) {
    int i = 0;
    while (b[i] != '\0') {
        a[i] = b[i];
        i++;
    }
    a[i] = '\0';
    printf("Copied String: %s", a);
}
