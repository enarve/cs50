#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int valid_key(string key);
string encode(string text, string key);
int get_div(char c);

int const length = 26;

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }
    else
    {
        string key = argv[1];
        if (strlen(key) != length)
        {
            printf("Key must contain %i characters.\n", length);
            return 1;
        }
        else if (valid_key(key) != 0)
        {
            printf("Key is not valid :(\n");
            return 1;
        }
        else
        {
            string text = get_string("plaintext: ");
            string ciphertext = encode(text, key);
            printf("ciphertext: %s\n", ciphertext);
        }
    }
    return 0;
}

int valid_key(string key)
{
    int flagarray[length];
    for (int i = 0; i < length; i++)
    {
        flagarray[i] = 0;
    }

    for (int i = 0; i < strlen(key); i++)
    {
        char c = key[i];
        if (!isalpha(c))
        {
            return 1;
        }
        int div = get_div(c);
        int index = c - div;
        if (flagarray[index] == 1)
        {
            for (int j = 0; j < length; j++)
            {
                printf("%i ", flagarray[j]);
            }
            printf("\n");
            return 1;
        }
        else
        {
            flagarray[index] = 1;
        }
    }
    return 0;
}

string encode(string text, string key)
{
    string cipher = text;
    for (int i = 0; i < strlen(text); i++)
    {
        char c = text[i];
        if (isalpha(c))
        {
            int div = get_div(c);
            int index = c - div;
            char encsym = key[index];
            if (islower(c))
            {
                encsym = tolower(encsym);
            }
            else
            {
                encsym = toupper(encsym);
            }
            cipher[i] = encsym;
        }
        else
        {
            cipher[i] = c;
        }
    }
    return cipher;
}

int get_div(char c)
{
    int div;
    if (isupper(c))
    {
        div = 65;
    }
    else
    {
        div = 97;
    }
    return div;
}
