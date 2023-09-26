###Taken from Feedback Session Block II - 24 september 2023

# I took the code named clean_text_general from the feedback session and I made 
# very small changes in the naming of the variables. The code in the feedback 
# session looked already quite similar in idea to the code I wrote for Assignment 2, 
# but the one in the feedback session is a bit more efficient and clear, so 
# therefore I use that one.

def preprocess(text: str, punct_to_remove, /):
    """
    Removes punctuation characters from a given text string.
    
    :param text: a string of text you wish to preprocess
    :param punct_to_remove: the punctuation characters you wish to remove
    :return: a preprocessed string of text removed from its punctuation characters
    """
    
    # assigning the text to a new variable to improve readability and clarity of the code
    preprocessed_text = text
    
    # iteration over all punctuation characters
    for punct in punct_to_remove:
        preprocessed_text = preprocessed_text.replace(punct, '') # replace all punctuation characters in text with empty str

    # return the preprocessed text
    return preprocessed_text

###