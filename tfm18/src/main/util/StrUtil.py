

def replace_last(original_str, old: str, new: str, occurrences: int) -> str:
    """
    Returns a string with the last specified occurences of a pattern replaced with another string.

    Credits: https://stackoverflow.com/a/2556252

    :param original_str: The original string.
    :param old: The replace match pattern.
    :param new: The string to replace the replace pattern.
    :param occurrences: Number of occurences >= 0.
    :return: The resulting string from replacing the last occureces of a pattern.
    """
    li = original_str.rsplit(sep=old, maxsplit=occurrences)
    return new.join(__iterable=li)
