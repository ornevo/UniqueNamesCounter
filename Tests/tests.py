"""
Testings
"""
import random
import string

import sys
import os
sys.path.append(os.path.dirname(__file__) + "/../")

from solution import count_unique_names


# Constants
NUM_OF_CHECKS = 1000
FUZZINESS = 0.3
MIN_SUCCESS_RATE = 0.8


def fuzz_string(s):
    indexes_to_mod = []

    for index in range(int(len(s)*FUZZINESS)):
        indexes_to_mod.append(random.choice(range(len(s))))

    for index in range(len(s)):
        # For each occurence of i in the indexes to modify
        for j in range(indexes_to_mod.count(index)):
            # Either insert a new character or modify an existing one
            fuzz_char = random.choice(string.lowercase)
            if random.choice([0, 1]):  # If insert
                s = s[:j] + fuzz_char + s[j:]
            else:
                s = s[:j] + fuzz_char + s[j+1:]

    return s


# Basic ones
assert count_unique_names("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli") == 1
assert count_unique_names("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli") == 1
assert count_unique_names("Deborah", "Egni", "Deborah", "Egli", "Deborah Egli") == 1
assert count_unique_names("Deborah S", "Egli", "Deborah", "Egli", "Egli Deborah") == 1 
assert count_unique_names("Michele", "Egli", "Deborah", "Egli", "Michele Egli") == 2


# Generated ones
first_names = []  # A list of lists, each sub-list is a list of equal nicknames
last_names = []  # A list of last names

# Read the datasets
with open("./nicknames.csv", "rt") as f:
    for line in f.read().split("\n"):
        first_names.append(line.split(","))
with open("./lastnames.csv", "rt") as f:
    last_names = f.read().split("\n")

# Generate random tests
success_count = 0
for i in xrange(NUM_OF_CHECKS):
    first_name_nicks = random.choice(first_names)
    last_name = random.choice(last_names)

    n1 = random.choice(first_name_nicks), last_name
    n2 = random.choice(first_name_nicks), fuzz_string(last_name)
    n3 = fuzz_string(n1[0] + " " + n1[1])

    success_count += (count_unique_names(n1[0], n1[1], n2[0], n2[1], n3) == 1)

success_rate = float(success_count) / NUM_OF_CHECKS
assert success_count >= MIN_SUCCESS_RATE


print "Success"
