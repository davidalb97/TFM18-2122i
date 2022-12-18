from datetime import timedelta


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
    return new.join(li)


def format_time_delta(time_delta: timedelta) -> str:
    """Converts the number of milliseconds to HH:MM:SS,ms time"""
    """Credits: Niel Godfrey Ponciano"""
    time_str = str(time_delta) + ".000"
    time_str_split = time_str.split(".", maxsplit=1)
    return f"{time_str_split[0]},{time_str_split[1][:3]}"


def format_millis(millis: float) -> str:
    return format_time_delta(time_delta=timedelta(milliseconds=millis))
