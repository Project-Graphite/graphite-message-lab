import re

BLOCKED_TERMS = frozenset(
    {
        "asshole",
        "bitch",
        "cunt",
        "dick",
        "fuck",
        "motherfucker",
        "nigger",
        "pussy",
        "shit",
        "slut",
        "whore",
    }
)


def contains_flagged_language(value):
    words = set(re.findall(r"[a-z0-9']+", value.casefold()))
    return not words.isdisjoint(BLOCKED_TERMS)
