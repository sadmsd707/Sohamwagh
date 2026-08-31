#include <stdio.h>

struct student {
    char name[10];
    int roll_no;
    int marks; 
};

int main() {
    struct student s[5];
    printf("Enter Information of 5 Students:\n");
    
    for(int i = 0; i < 5; i++) {
        printf("\nStudent %d", i + 1);
        printf("\nStudent Name: ");
        scanf("%s", s[i].name);
        
        printf("Enter Roll No: ");
        scanf("%d", &s[i].roll_no);
        
        printf("Enter Marks: ");
        scanf("%d", &s[i].marks); 
    }
    
    printf("\n--- Student Details ---\n");
    for(int i = 0; i < 5; i++) {
        printf("\nStudent %d", i + 1);
        printf("\nName: %s", s[i].name);
        printf("\nRoll No: %d", s[i].roll_no);
        printf("\nMarks: %d\n", s[i].marks);
    }
    
    return 0;
}


