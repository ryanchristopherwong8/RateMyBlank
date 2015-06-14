import re

def strip_non_alphanum(value):
    """
    remove all non alpha numeric
    """
    return re.sub('[^0-9a-zA-Z]+', '', value)