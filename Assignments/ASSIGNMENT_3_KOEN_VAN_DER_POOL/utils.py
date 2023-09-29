import glob
import operator
from nltk.tokenize import sent_tokenize, word_tokenize


def get_paths(input_folder: str, /):
    """
    A function to get a list of the pathnames of the text files stored in the given input folder.
    
    :param input_folder: a string of the pathname of the input folder for which you want to store the 
    file pathnames
    :return: a list of strings of the file pathnames
    """
    
    # initialising an empty list
    list_text_files = []
    
    # looping over the text files in the input folder
    for text_file in glob.glob(f"{input_folder}/*.txt"):
        list_text_files.append(text_file) # adding the pathnames of the files to the list
    
    # returning the list of pathnames
    return list_text_files


def get_basic_stats(txt_path, /):
    """
    Given a pathname of a text, this function returns a dictionary with
    basic statistics of the text.
    
    :param txt_path: the pathname of the text
    :return: a dictionary with basic statistics of the text
    """
    
    # initializing a dictionary 
    dict_basic_stats = {}
    
    # using a context manager to access the content of the file
    with open(txt_path, "r") as file:
        text = file.read()
    
    # splitting the text into sentences and counting the number of sentences
    sentences = sent_tokenize(text)
    num_sents = len(sentences)
    
    # tokenizing the text and counting the number of tokens
    tokens = word_tokenize(text)
    num_tokens = len(tokens)
   
    # getting the number of unique tokens using the set function and counting the unique tokens
    vocab = set(tokens)
    vocab_size = len(vocab)
    
    # depending on the book counting a specific word
    if txt_path == "../Data/books/HuckFinn.txt":
        num_chapters_or_acts = text.count('CHAPTER')
    elif txt_path == "../Data/books/AnnaKarenina.txt":
        num_chapters_or_acts = text.count('Chapter ')
    elif txt_path == "../Data/books/Macbeth.txt":
        num_chapters_or_acts = text.count('ACT')

    # initialize empty string
    token2freq = {}

    # loop over the words to count them and add them to the dictionary
    for token in tokens:
        if token in token2freq:
            token2freq[token] += 1
        else:
            token2freq[token] = 1
            
    # initialize empty list
    top_30_tokens = []

    # loop over 30 most frequent tokens and add this to the list top_30_tokens
    for token, freq in sorted(token2freq.items(), key=operator.itemgetter(1), reverse=True)[:30]:
        top_30_tokens.append(token)
    
    # adding the previous retrieved statistics to the dictionary
    dict_basic_stats['num_sents'] = num_sents
    dict_basic_stats['num_tokens'] = num_tokens
    dict_basic_stats['vocab_size'] = vocab_size
    dict_basic_stats['num_chapters_or_acts'] = num_chapters_or_acts
    dict_basic_stats['top_30_tokens'] = top_30_tokens
    
    # returning the dictionary
    return dict_basic_stats
