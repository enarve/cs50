#include <cs50.h>
#include <stdio.h>

int check_if_valid(long number);
int get_first_two_digits(long number);
int get_length(long number);

int main(void)
{
    string invalid_message = "INVALID\n";
    long number = get_long("Enter card number: ");
    int result = check_if_valid(number);
    if (result == 0)
    {
        printf("%s", invalid_message);
    }
    else
    {
        int code = get_first_two_digits(number);
        if (code / 10 == 4)
        {
            if (get_length(number) == 13 || get_length(number) == 16)
            {
                printf("VISA\n");
            }
            else
            {
                printf("%s", invalid_message);
            }
        }
        else if (code == 34 || code == 37)
        {
            if (get_length(number) == 15)
            {
                printf("AMEX\n");
            }
            else
            {
                printf("%s", invalid_message);
            }
        }
        else if (code == 51 || code == 52 || code == 53 || code == 54 || code == 55)
        {
            if (get_length(number) == 16)
            {
                printf("MASTERCARD\n");
            }
            else
            {
                printf("%s", invalid_message);
            }
        }
        else
        {
            printf("%s", invalid_message);
        }
    }
}

int check_if_valid(long number)
{
    long main_part = number;
    int rest_part = 0;
    int i = 1;
    int sum = 0;
    int second_sum = 0;
    while (main_part > 0)
    {
        rest_part = main_part % 10;
        main_part /= 10;
        if (i % 2 == 0)
        // Compute sum with digits multiplied by two
        {
            int n = rest_part * 2;
            do
            {
                int rn = n % 10;
                sum += rn;
                n /= 10;
            }
            while (n != 0);
        }
        else
        // Compute other sum
        {
            int n = rest_part;
            do
            {
                int rn = n % 10;
                sum += rn;
                n /= 10;
            }
            while (n != 0);
        }
        i++;
    }

    return (sum % 10 == 0);
}

int get_first_two_digits(long number)
{
    long n = number;

    while (n / 100 != 0)
    {
        n /= 10;
    }
    return n;
}

int get_length(long number)
{
    int i = 0;
    while (number / 10 != 0)
    {
        number /= 10;
        i++;
    }
    if (number != 0)
    {
        i++;
    }
    // printf("%i\n", i);
    return i;
}
