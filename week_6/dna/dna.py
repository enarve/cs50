import csv
import sys


def main():

    # Check for command-line usage
    if not len(sys.argv) == 3:
        print("Provide two arguments: dna.py <known_str_counts.csv> <sequence_to_identify.txt>")
        return

    # Read database file into a variable
    with open(sys.argv[1]) as db:
        reader = list(csv.reader(db))
        # print("reader", reader)
        if len(reader) > 0:
            strs = reader[0][1:]
            # print("strs", strs)

            # Read DNA sequence file into a variable
            with open(sys.argv[2]) as sequence:
                repeats = []
                text = sequence.read()
                # Find longest match of each STR in DNA sequence
                for str in strs:
                    repeat = f"{longest_match(text, str)}"
                    repeats.append(repeat)
                # Check database for matching profiles
                # print("repeats", repeats)
                for row in reader[1:]:
                    if row[1:] == repeats:
                        print(f"{row[0]}")
                        return

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
