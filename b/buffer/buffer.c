#include <stdio.h>
void flag()
{
    printf("Congrats! you got the flag\n");
}

void print()
{
    char buffer[6];
    printf("Enter payload :\n");
    gets(buffer); // buffer overflow vulnerability
}

int main()
{       
    print();
    return 0;
}