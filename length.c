#include <stdio.h>
int length(char[]);
int main() {
    char str[50];
    printf("Enter String: ");
    scanf("%s", str);
    printf("Length of the String is %d", length(str));
    return 0;
}
int length(char a[]) {
    int len = 0;
