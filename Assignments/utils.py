from lxml import etree as et


def load_root(path, /):
    """Find the root of an xml file given a filepath (str). """
    tree = et.parse(path)
    root = tree.getroot()
    return root


def get_talks(root, /):
    """Get all talk elements from an xml file."""
    talks = root.findall('file')
    return talks


def get_title(talk, /):
    """
    Finds the title of a given talk.

    :param talk: the talk given as an XML element
    :return: the title of the talk as a str
    """
    # Define the path to the title element
    path_to_title = './head/title'

    # Find the title element
    title_element = talk.find(path_to_title)

    # Check if title element exists
    if title_element is not None:
        # If element exists, extract its text
        title = title_element.text
    else:
        title = "No title available"

    return title


def get_id(talk, /):
    """
    Finds the ID of a given talk.

    :param talk: the talk given as an XML element
    :return: the ID of the talk as a str
    """
    # Define the path to the talk ID element
    path_to_id = './head/talkid'

    # Find the talk ID element
    talk_id_element = talk.find(path_to_id)

    # Check if talk ID element exists
    if talk_id_element is not None:
        # If element exists, extract its text
        talk_id = talk_id_element.text
    else:
        talk_id = "No talk ID available"

    return talk_id


def get_date(talk, /):
    """
    Finds the date of a given talk.

    :param talk: the talk given as an XML element
    :return: the date of the talk as a str
    """
    # Define the path to the date element
    path_to_date = './head/date'

    # Find the date element
    date_element = talk.find(path_to_date)

    # Check if data element exists
    if date_element is not None:
        # If element exists, extract its text
        date = date_element.text
    else:
        date = "No date available"

    return date


def get_word_count(talk, /):
    """
    Finds the word count of a given talk.

    :param talk: the talk given as an XML element
    :return: the word count of the talk as an int
    """
    # Define the path to the wordnum element
    path_to_word_num = './head/wordnum'

    # Find the wordnum element
    word_num_element = talk.find(path_to_word_num)

    # Check if wordnum element exists
    if word_num_element is not None:
        # If element exists, extract text of the wordnum element and cast to int
        word_num = int(word_num_element.text)
    else:
        word_num = "No word count available"

    return word_num


def get_mean_word_count(list_of_word_counts, /):
    """
    Calculates the mean word count out of a list of word counts.

    :param list_of_word_counts: all the word counts as a list of integers
    :return: the mean word count
    """
    # Initialize a count
    count = 0

    # Add each word count in the list to the count
    for word_count in list_of_word_counts:
        count += word_count

    # Divide the count by the length of the word count list to get the mean
    mean = count / len(list_of_word_counts)

    return mean


def get_speaker(talk, /):
    """
    Finds the speaker of a given talk.

    :param talk: the talk given as an XML element
    :return: the speaker of the talk as a str
    """
    # Define the path to the speaker element
    path_to_speaker = './head/speaker'

    # Find the speaker element
    speaker_element = talk.find(path_to_speaker)

    # Check if speaker element exists
    if speaker_element is not None:
        # If element exists, extract text of the speaker element
        speaker = speaker_element.text
    else:
        speaker = "Speaker text not available"

    return speaker


def get_int_date(date, /):
    """
    Converts a 'YYYY/MM/DD' date string to three integers representing the year, month, and day.

    :param date: the date of a talk as a str in the format 'YYYY/MM-/DD'
    :return: the year, the month, and the day of the date as integers
    """
    # Split the three components of the date string into a list of strings
    split_date = date.split('/')

    # Cast each element in the list to an integer
    year = int(split_date[0])
    month = int(split_date[1])
    day = int(split_date[2])

    return year, month, day


def compare_dates(selected_date, current_date, /):
    """
    Checks whether the current date is older than, newer than or the same as the selected date.

    :param selected_date: the date of the selected talk as a str in the format 'YYYY/MM-/DD'
    :param current_date: the date of the current talk as a str in the format 'YYYY/MM-/DD'
    :return: a str denoting if the current date is older than, newer than or the same as the selected date
    """
    # Convert the str dates to integer components
    selected_year, selected_month, selected_day = get_int_date(selected_date)
    current_year, current_month, current_day = get_int_date(current_date)

    # Check if current date is newer than the selected date
    if current_year > selected_year or (current_year == selected_year
                                        and ((current_month > selected_month)
                                             or (current_month == selected_month
                                                 and current_day > selected_day))):
        result_comparison = "newer"
    # Check if current date is the same as the selected date
    elif current_year == selected_year and current_month == selected_month and current_day == selected_day:
        result_comparison = "same"
    # If neither of the previous two conditions are true, then the current date is older than the selected one
    else:
        result_comparison = "older"

    return result_comparison


def get_title_id_tuples(selected_titles, id_to_title, /):
    """
    Extracts the talk IDs for selected talk titles from a provided dictionary.

    :param selected_titles: list of talk titles you are interested in
    :param id_to_title: dict with a ID-to-title mapping
    :return: a list of tuples containing talk titles and IDs
    """
    # Create empty list to store the title-ID tuples in
    title_id_tuples = []

    # Loop over all ID-to-title mapping
    for talk_id, title in id_to_title.items():
        # Add (title, talk_id) tuple if title is in list of selected titles
        if title in selected_titles:
            title_id_tuples.append((title, talk_id))

    return title_id_tuples
