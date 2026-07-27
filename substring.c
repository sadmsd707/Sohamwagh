#include <stdio.h>
int length(char[]);
void substring(char[], char[]);
int main() {
    char str[50], sub[50];
    printf("Enter String A : ");
    scanf("%s", str);

    printf("Enter B : ");
    scanf("%s", sub);
    substring(str, sub);
    return 0;
}
int length(char a[]) {
    int len = 0;
    while (a[len] != '\0') {
        len++;
    }
    return len;
}
void substring(char a[50], char b[50]) {
    int al = length(a);
    int bl = length(b);
    int i, j;
    int flag = 0;

    for (i = 0; i <= al - bl; i++) {
        for (j = 0; j < bl; j++) {
            if (a[i + j] != b[j])
                break;
        }
        if (j == bl) {
            flag = 1;
            break;
        }
    }
    if (flag == 1)
        printf("The String B is a substring of String A");
    else
        printf("The String B is not a substring of String A");
}
