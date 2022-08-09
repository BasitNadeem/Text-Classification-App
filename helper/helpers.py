def is_ascii(s):
    """
    function that checks if a string is 
    ascii character or not.

    input:
            s: string

    output:

    """
    return all(ord(c) < 128 for c in s)


import re


def process_title(title):
    """
    function that extracts characters and numbers
    from strings.

    input:
            title: string value

    output:
            title: cleaned string value
    """
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_“.|"'''

    for ele in punc:
        if ele in title:
            title = title.replace(ele, "")
    # strip away numbers and parenthesis
    title = (
        title.replace("(", "")
        .replace(")", "")
        .replace("/", "")
        .replace("_", "")
        .replace("-", "")
        .replace("&", "")
        .replace(":", "")
        .replace("@", "")
    )
    title = re.sub(r"\d+", "", title)
    title = title.replace("?", "")
    # strip away "part" word
    title = re.sub(r"[Pp]art", "", title)
    # strip II and III and IV
    title = title.replace("II", "").replace("III", "").replace("IV", "")
    title = title.strip()
    title = re.sub(" +", " ", title)

    return title