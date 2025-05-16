#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

float average_letters(string text);
float average_sentences(string text);
int calculate_grade(float avl, float avs);

const int min_grade = 1;
const int max_grade = 16;

int main(void)
{
    // Get input
    string text = get_string("Input text: ");

    // Calculate grade
    float avl = average_letters(text);
    float avs = average_sentences(text);
    int grade = calculate_grade(avl, avs);

    // Print result
    if (grade < min_grade)
    {
        printf("Before Grade %d\n", min_grade);
    }
    else if (grade >= max_grade)
    {
        printf("Grade %d+\n", max_grade);
    }
    else
    {
        printf("Grade %d\n", grade);
    }
}

int calculate_grade(float avl, float avs)
{
    int grade = round(100 * (0.0588 * avl - 0.296 * avs) - 15.8);
    return grade;
}

float average_letters(string text)
{
    int space_counter = 0;
    int letter_counter = 0;

    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isspace(text[i]))
        {
            space_counter++;
        }
        if (!isspace(text[i]) && !ispunct(text[i]))
        {
            letter_counter++;
        }
    }
    float avl = (float) letter_counter / (float) (space_counter + 1);
    // printf("avl %f\n", avl);
    return avl;
}

float average_sentences(string text)
{
    int point_counter = 0;
    int space_counter = 0;

    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            point_counter++;
        }
        if (isspace(text[i]))
        {
            space_counter++;
        }
    }
    float avs = (float) point_counter / (float) (space_counter + 1);
    // printf("avs %f\n", avs);
    return avs;
}
