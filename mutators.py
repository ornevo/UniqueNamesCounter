from itertools import permutations


# Taken from http://fm.schmoller.net/2010/01/if-ever-you-need-a-really-comprehensive-title-drop-down.html
HONORIFICS = [
    "mr",
    "mister",
    "miss",
    "mrs",
    "ms",
    "mx",
    "dr",
    "sir",
    "dame",
    "prof",
    "professor",
    "rabbi",
    "canon",
    "chief",
    "sister",
    "reverend",
    "major",
    "cllr",
    "baroness",
    "captain",
    "master",
    "lady",
    "mp"
]


def remove_honorific(names):
    for name in names:
        for honorific in HONORIFICS:
            if name.startswith(honorific + " "):
                name_with_no_honor = " ".join(name.split(" ")[1:])
                names.append(name_with_no_honor)


def remove_middle_name(names):
    for name in names:
        splt_name = name.split(" ")
        if len(splt_name) > 2:
            name_with_no_middle = splt_name[1] + " " + " ".join(splt_name[2:])
            names.append(name_with_no_middle)


def reorder_names(names):
    start_len = len(names)
    for i in range(start_len):
        name = names[i]
        perms = [" ".join(x) for x in permutations(name.split(" "))]
        names.extend(perms)


# The order doesn't matter.
mutators = [remove_honorific, remove_middle_name, reorder_names]
