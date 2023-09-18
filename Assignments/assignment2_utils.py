def clean_text_general(text, /, chars_to_remove={'\n', ',', '.', '"'}):
    """
    Preprocesses a given str text by replacing a set of given characters by the empty str.

    :param text: str of text
    :param chars_to_remove: a set of characters to be removed from the text
    :return: str of text cleared of a set of characters
    """
    for char in text:
        if char in chars_to_remove:
            text = text.replace(char, '')
    return text