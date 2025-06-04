// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 77;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    unsigned int h = hash(word);
    node* ptr = table[h];
    while (ptr != NULL)
    {
        if (strcasecmp(ptr->word, word) == 0)
        {
            return true;
        }
        else
        {
            ptr = ptr->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned int res = toupper(word[0]) - 'A';
    if (strlen(word) > 1)
    {
        if (isalpha(word[1]))
        {
            res += toupper(word[1]) - 'A';
        }
    }
    return res;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE* input = fopen(dictionary, "r");
    if (input == NULL)
    {
        return false;
    }
    char word[LENGTH];

    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    while (fscanf(input, "%s", word) != EOF)
    {
        // add to hash table
        unsigned int h = hash(word);

        node* n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n->word, word);

        if (table[h] == NULL)
        {
            table[h] = n;
            n->next = NULL;
        }
        else
        {
            node* temp = table[h];
            table[h] = n;
            n->next = temp;
        }

    }

    fclose(input);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    int count = 0;
    for (int i = 0; i < N; i++)
    {
        node* ptr = table[i];
        while (ptr != NULL)
        {
            ptr = ptr->next;
            count++;
        }
    }
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node* ptr = table[i];
        while (ptr != NULL)
        {
            node* tmp = ptr;
            tmp = ptr->next;
            free(ptr);
            ptr = tmp;
        }
    }
    return true;
}
