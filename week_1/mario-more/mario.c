#include <cs50.h>
#include <stdio.h>

void make_row(int height, int unit);
void make_left_half(int height, int unit);
void make_right_half(int unit);

int main(void)
{
    int height;
    // Wait for positive number by user
    do
    {
        height = get_int("Choose height: ");
    }
    while (height < 1 || height > 8);

    // Build the pyramid
    for (int i = 0; i < height; i++)
    {
        make_row(height, i + 1);
    }
}

void make_row(int height, int unit)
{
    make_left_half(height, unit);
    printf("  ");
    make_right_half(unit);
    printf("\n");
}

void make_left_half(int height, int unit)
{
    for (int i = height - unit; i > 0; i--)
    {
        printf(" ");
    }
    for (int i = 0; i < unit; i++)
    {
        printf("#");
    }
}

void make_right_half(int unit)
{
    for (int i = 0; i < unit; i++)
    {
        printf("#");
    }
}
