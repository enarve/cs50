#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int recover(char *filename);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s filename\n", argv[0]);
        return 1;
    }
    else
    {
        return recover(argv[1]);
    }
}

int recover(char *filename)
{
    printf("%s\n", filename);
    FILE *input = fopen(filename, "r");
    FILE *output = NULL;
    if (input == NULL)
    {
        printf("File not found!\n");
        return 1;
    }
    else
    {
        // Prepare buffer for memory
        const int block_size = 512;
        uint8_t block[block_size];
        uint8_t sign_head[] = {0xff, 0xd8, 0xff};
        uint8_t sign_tails[] = {0xe0, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7,
                                0xe8, 0xe9, 0xea, 0xeb, 0xec, 0xed, 0xee, 0xef};
        int counter = 0;
        int output_open = 0;

        // Read input
        while (fread(block, block_size, 1, input))
        {
            int head =
                (block[0] == sign_head[0] && block[1] == sign_head[1] && block[2] == sign_head[2]);
            int tail = 0;

            if (head)
            {
                for (int i = 0, len = (sizeof(sign_tails) / sizeof(uint8_t)); i < len; i++)
                {
                    if (sign_tails[i] == block[3])
                    {
                        tail = 1;
                    }
                }
            }

            if (head && tail)
            {
                // Close old output if exists
                if (output != NULL)
                {
                    fclose(output);
                }
                // Start new output
                char output_name[7];
                char *ext = "jpg";
                sprintf(output_name, "%03i.%s", counter, ext);
                output = fopen(output_name, "w");
                counter++;
                fwrite(block, block_size, 1, output);
            }
            else
            {
                // Write to output if exists
                if (output != NULL)
                {
                    fwrite(block, block_size, 1, output);
                }
            }
        }

        // Close files
        fclose(output);
        fclose(input);
        return 0;
    }
}
