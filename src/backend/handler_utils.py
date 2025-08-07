import re


def clean_lection_list(SQLite_output: list[tuple[str]]) -> list[int]:
    """
    Extracts the numbers of the lection from the raw output.

    Args:
        SQLite_output (list[tuple[str]]): The raw output from the SQLite3 function.

    Returns:
        list[int]: Only the number of the lections.
    """
    word_list: list[str] = []
    number_list: list[int] = []
    for entry in SQLite_output:
        for word in entry:
            word_list.append(word)

    for entry in word_list:
        number_list.append(int(re.search(r"\d+", entry).group()))

    return number_list
