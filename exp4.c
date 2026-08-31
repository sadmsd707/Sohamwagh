#include <stdio.h>

struct student{
    char name[10];
    int roll_no;
    int marks;
};

int main() {
    struct student s[3];
    
    for(int i=0;i<3;i++) {
         printf("Student Name:");
         scanf("%s",&s[i].name);
         printf("Enter Roll No:");
         scanf("%d",&s[i].roll_no);
         printf("Enter Marks:");
         scanf("%f",&s[i].marks);
    }

    return 0;

}
