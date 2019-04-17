def case_insensitive_lookup(d, text):
    # Lookup a string key from a dictionary without regard to the case
    # of the string
    text = text.lower()
    return d[text]
