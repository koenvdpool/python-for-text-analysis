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

    """
    path_to_title = './head/title'

    title_element = talk.find(path_to_title)

    if title_element is not None:
        title = title_element.text
    else:
        title = "No title available"

    return title


def get_id(talk, /):
    """

    """
    path_to_id = './head/talkid'

    talk_id_element = talk.find(path_to_id)

    if talk_id_element is not None:
        talk_id = talk_id_element.text
    else:
        talk_id = "No talk ID available"

    return talk_id


def get_date(talk, /):
    """

    """
    path_to_date = './head/date'

    date_element = talk.find(path_to_date)

    if date_element is not None:
        date = date_element.text
    else:
        date = "No date available"

    return date


def get_word_count(talk, /):
    """

    """
    path_to_word_num = './head/wordnum'

    word_num_element = talk.find(path_to_word_num)

    word_num = int(word_num_element.text)

    return word_num


def get_mean_word_count(list_of_word_counts, /):
    """

    """
    count = 0

    for word_count in list_of_word_counts:
        count += word_count

    mean = count / len(list_of_word_counts)

    return mean


def get_speaker(talk, /):
    """

    """
    path_to_speaker = './head/speaker'

    speaker_element = talk.find(path_to_speaker)

    speaker = speaker_element.text

    return speaker


def get_int_date(date, /):
    """

    """
    split_date = date.split('/')

    year = int(split_date[0])
    month = int(split_date[1])
    day = int(split_date[2])

    return year, month, day


def compare_dates(selected_date, current_date, /):
    """

    """
    selected_year, selected_month, selected_day = get_int_date(selected_date)
    current_year, current_month, current_day = get_int_date(current_date)

    if current_year > selected_year or (current_year == selected_year
                                        and ((current_month > selected_month)
                                             or (current_month == selected_month
                                                 and current_day > selected_day))):
        result_comparison = "newer"
    elif current_year == selected_year and current_month == selected_month and current_day == selected_day:
        result_comparison = "same"
    else:
        result_comparison = "older"

    return result_comparison
