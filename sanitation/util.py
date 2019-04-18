import re


def case_insensitive_lookup(d, text):
    # Lookup a string key from a dictionary without regard to the case
    # of the string
    text = text.lower()
    return d[text]


# Remove the HTML tags from the response text
# Returns the text with the tags removed
def strip_html_tags(html):
    prog = re.compile(r"<.*?>")
    return prog.sub("", html)
