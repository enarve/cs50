#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int count_score(string word);

const int points[] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                      1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int main(void)
{
    // Prompt for the words
    string word1 = get_string("First word: ");
    string word2 = get_string("Second word: ");

    // Count scores
    int score1 = count_score(word1);
    int score2 = count_score(word2);

    // Print the winner
    if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int count_score(string word)
{
    int score = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        int letter = tolower(word[i]);
        if (isalpha(letter))
        {
            int index = letter - 97;
            int p = points[index];
            score += p;
        }
    }
    // printf("%i\n", score);
    return score;
}
