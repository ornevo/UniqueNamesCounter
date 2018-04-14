DEP_ERR = '''
ERROR: Not all dependencies are met. please install:
    sudo pip install python-Levenshtein Metaphone
'''
DEBUG = False
# The similarity score which two strings are accounted as equal if their score is below it
MUTATIONS_SIMILARITY_THRESHOLD = 0.4
# The similarity score which two metaphone codes are accounted as equal if their score is below it
METAPHONE_SIMILARITY_THRESHOLD = 0.2

import sys
import mutators

try:
    import Levenshtein
    import metaphone
except ImportError as e:
    print DEP_ERR
    exit(1)


def get_similarity(name_a, name_b):
    """
    This function calculates the Levenshtein distance of the two names, divided by the max length of them.
    This is the ratio of the similar parts to the different parts
    :param name_a: The first name
    :param name_b: The second name
    :return: The Levenshtein distance of the two names, divided by the their max length.
    """
    return Levenshtein.distance(name_a, name_b) / float(max(len(name_a), len(name_b)))


def get_metaphone_codes(mutations):
    """
    This function receives a list of strings and return a list of matching Metaphone codes
    :param mutations: The list of the mutations
    :return: A list of Metaphone codes for each mutation in the mutations list
    """
    ret = []

    # Since double-Metaphone returns a tuple of two possibilities, add them both using extend
    for mutation in mutations:
        metaphone_codes = metaphone.doublemetaphone(mutation)  # A tuple of two options
        ret.extend(metaphone_codes)

    # Remove spaces
    return filter(lambda mut: mut, ret)


def compare(first_name, second_name):
    """
    This function checks and returns whether those two names are different or the same.

    The function works as follows:
        1. Lowercase the names, strip them and discard any special characters. Those don't make different
            names and may only add noise.
        2. Create mutations of the names using several modifiers, such as removing honorifics
             and removing middle names
        3. Create for each new mutation a string which represents their English verbal pronunciation, using
            the Metaphone algorithm
        4. Compare all mutations of the first name with the mutations of the second name, and find the
            minimum distance among those

    :param first_name: The first name of the comparison
    :param second_name: The second name of the comparison
    :return: True if the names are the same, False otherwise
    """
    # Step 1 - Lower case and discard special characters
    first_mutations = [filter(lambda char: char.isalnum() or char == ' ', first_name.lower().strip())]
    second_mutations = [filter(lambda char: char.isalnum() or char == ' ', second_name.lower().strip())]

    # Step 2 - Create all mutations
    for mutator in mutators.mutators:
        mutator(first_mutations)
        mutator(second_mutations)

    # Step 3 - Find a string representation of the verbal pronunciation of each mutation
    first_mutations_metaphone = get_metaphone_codes(first_mutations)
    second_mutations_metaphone = get_metaphone_codes(second_mutations)

    # Step 4 - Compare the first name's and the second name's mutations
    # First create a list of matches (first_name_mutation, second_name_mutation)
    mut_matches = [(first_mut, second_mut) for first_mut in first_mutations for second_mut in second_mutations]
    metaphone_matches = [(first_meta, second_meta) for first_meta in first_mutations_metaphone
                         for second_meta in second_mutations_metaphone]

    # Remove duplicates
    mut_matches = set(mut_matches)
    metaphone_matches = set(metaphone_matches)

    # Find most similar mutations
    muts_best = min([get_similarity(match[0], match[1]) for match in mut_matches])
    metaphones_best = min([get_similarity(match[0], match[1]) for match in metaphone_matches])

    if DEBUG:
        print "Scores for \"{0}\" V.S. \"{1}\":\n\tRegular score: {2}\n\tMetaphore score: {3}" \
            .format(first_name, second_name, muts_best, metaphones_best)

    # Return whether one of the matches got a good enough score
    return muts_best < MUTATIONS_SIMILARITY_THRESHOLD or metaphones_best < METAPHONE_SIMILARITY_THRESHOLD


def count_unique_names(bill_first_name, bill_last_name, ship_first_name, ship_last_name, bill_name_on_card):
    """
    This function calculates the number of unique names passed to it as parameters.

    :param bill_first_name: The first name in the billing address form (could include middle names)
    :param bill_last_name: The last name in the billing address form
    :param ship_first_name: The first name in the shipping address form (could include middle names)
    :param ship_last_name: The last name in the shipping address form
    :param bill_name_on_card: The full name as it appears on the credit card
    :return: The number of supplied names.
    """
    bill_name = bill_first_name + " " + bill_last_name
    ship_name = ship_first_name + " " + ship_last_name

    comparisons = [compare(bill_name, ship_name),
                   compare(bill_name, bill_name_on_card),
                   compare(ship_name, bill_name_on_card)]

    return max(1, 3 - sum(comparisons))


def main():
    global DEBUG
    DEBUG = True

    if len(sys.argv) != 6:
        print "Usage: " + sys.argv[0] + \
              ' "<billFirstName>" "<billLastName>" "<shipFirstName>" "<shipLastName>" "<billNameOnCard>"'
        exit(1)

    print "There are " + str(count_unique_names(*sys.argv[1:])) + " supplied unique names."


if __name__ == "__main__":
    main()
