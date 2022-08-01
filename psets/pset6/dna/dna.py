import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print('Usage: python dna.py data.csv sequence.txt')

    # TODO: Read database file into a variable
    with open(sys.argv[1]) as x:
        reader = csv.reader(x)
        db = list(reader)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2]) as y:
        sequence = y.read()

    # TODO: Find longest match of each STR in DNA sequence
    z = []
    for i in range(1, len(db[0])):
        z.append(longest_match(sequence, db[0][i]))

    # TODO: Check database for matching profiles
    s = 'No match'
    counter = 0
    for i in range(1, len(db)):
        for j in range(len(z)):
            if z[j] == int(db[i][j+1]):
                counter +=1
        if counter == len(z):
            s = db[i][0]
            break
        else:
            counter = 0
    print(s)

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
