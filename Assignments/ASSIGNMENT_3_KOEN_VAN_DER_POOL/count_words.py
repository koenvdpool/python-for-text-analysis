from utils_3a import preprocess

# Defining the function with two positional parameters
def my_word_count(text: str, punct_to_remove, /):
    """
    Given a string of text, this function cleans the text from its punctuation and returns 
    a dictionary containing the words used it the text and their respective counts. 
    
    :param text: a string of text for which you want to determine the word count
    :param punct_to_remove: the punctuation characters you wish to remove from the text
    :return: a dictionary of the words used in the text and their respective counts
    """
    # initialise dictionary
    word2freq = {}
    
    # call the function preprocess to have the string text cleaned from punctuation
    preprocessed_text = preprocess(text, punct_to_remove) 
    
    # split the preprocessed text into words
    words = preprocessed_text.split(' ')
    
    # loop over the words to count them and add them to the dictionary
    for word in words:
        if word in word2freq:
            word2freq[word] += 1
        else:
            word2freq[word] = 1
            
    # returning the dictionary        
    return word2freq


# Assigning a paragraph of text to the variable to test the function with
a_paragraph = 'There was a man on the corner of the street, sitting on a bench. The man seemed lost in thought, reflecting on all the lives he had lived in the past. The bench was cold and had raindrops glistening on its surface. With a book in his hand, the man was ready to live another life.'

# We call the function and assign the resulting string to word_count_a_paragraph
word_count_a_paragraph = my_word_count(a_paragraph, {',', '.', '"', '?', '!', ':', ';'})

# We print the result
print(word_count_a_paragraph)