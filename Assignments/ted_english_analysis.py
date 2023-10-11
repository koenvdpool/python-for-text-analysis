import utils


def find_wc(talk_elements, /, length="longest"):
    """
    Finds the talk(s) that is/are either the longest or shortest in word count.

    :param talk_elements: list of talk elements
    :param length: specifies the desired talk length, either "longest" or "shortest" (default is "longest")
    :return: lists of title(s) and ID(s) for the selected talk(s), the word count of the selected talk(s),
    and the average word count over all the talks
    """
    # Create variables to store the selected word count (highest or lowest) and its corresponding talk(s)
    selected_word_count = 0
    selected_talks = []

    # Create variable to store all word counts
    all_word_counts = []

    # Loops over all the talks
    for talk in talk_elements:
        current_word_count = utils.get_word_count(talk)
        # Check if talk has text, if not, continue to next talk
        if current_word_count <= 0:
            continue

        # Append word count to the list of all word counts
        all_word_counts.append(current_word_count)

        # Compare the word count of the current talk to the selected word count
        if length == "longest":
            if current_word_count > selected_word_count:
                # If longer, adjust the selected word count and list of selected talks
                selected_word_count = current_word_count
                selected_talks = [talk]
            elif current_word_count == selected_word_count:
                # If the word count is the same, append talk to the list of selected talks
                selected_talks.append(talk)

        elif length == "shortest":
            if (selected_word_count == 0) or (current_word_count < selected_word_count):
                # If zero or shorter, adjust the selected word count and list of selected talks
                selected_word_count = current_word_count
                selected_talks = [talk]
            elif current_word_count == selected_word_count:
                # If the word count is the same, append talk to the list of selected talks
                selected_talks.append(talk)

    # Create lists to store the titles and IDs of the selected talks
    selected_titles = []
    selected_ids = []

    # Get mean word count over all the talks
    mean_word_count = utils.get_mean_word_count(all_word_counts)

    # Loops over the selected talk and add titles and IDs to the lists
    for talk in selected_talks:
        title = utils.get_title(talk)
        selected_titles.append(title)
        talk_id = utils.get_id(talk)
        selected_ids.append(talk_id)

    # Return the titles, IDs, word count and mean word count
    return selected_titles, selected_ids, selected_word_count, mean_word_count


def find_date(talk_elements, /, time="oldest"):
    """
    Finds either the oldest or newest talk(s).

    :param talk_elements: list of talk elements
    :param time: specifies if you want the "oldest" of "newest" talk(s) (default is "oldest")
    :return: the title(s) and ID(s) of the selected talk(s) as two lists
    """

    # Create variables to store the selected date (oldest or newest) and its corresponding talk(s)
    selected_date = ''
    selected_talks = []

    # Loops over all the talks
    for talk in talk_elements:
        word_count = utils.get_word_count(talk)
        # Check if talk has text, if not, continue to next talk
        if word_count <= 0:
            continue

        # Get the date of the current talk
        current_date = utils.get_date(talk)

        # Check for current talk if date exists
        if current_date != "No date available":
            # If list of selected talks is empty, adjust the selected data and add current talk to the list
            if not selected_talks:
                selected_date = current_date
                selected_talks = [talk]
            else:
                # Compare the dates of the selected talk(s) and the current talk
                dates_comparison = utils.compare_dates(selected_date, current_date)
                if time == "newest":
                    if dates_comparison == 'newer':
                        # If newer, adjust the selected date and list of selected talks
                        selected_date = current_date
                        selected_talks = [talk]
                    elif dates_comparison == 'same':
                        # If the date is the same, append talk to the list of selected talks
                        selected_talks.append(talk)

                if time == "oldest":
                    if dates_comparison == 'older':
                        # If older, adjust the selected date and list of selected talks
                        selected_date = current_date
                        selected_talks = [talk]
                    elif dates_comparison == 'same':
                        # If the date is the same, append talk to the list of selected talks
                        selected_talks.append(talk)

    # Create lists to store the titles and IDs of the selected talks
    selected_titles = []
    selected_ids = []

    # Loops over the selected talk and add titles and IDs to the lists
    for talk in selected_talks:
        title = utils.get_title(talk)
        selected_titles.append(title)
        talk_id = utils.get_id(talk)
        selected_ids.append(talk_id)

    # Returns the title(s) and ID(s) of the selected talk(s)
    return selected_titles, selected_ids


def find_speaker(talk_elements, /):
    """
    Finds the speakers with more than one talk.

    :param talk_elements: list of talk elements
    :return: a dict of the speakers mapped to their talks
    """
    # Create dict to map the speakers to their talks
    speaker_to_talks = {}

    # Loops over the talks
    for talk in talk_elements:
        word_count = utils.get_word_count(talk)
        # Check if talk has text, if not, continue to next talk
        if word_count <= 0:
            continue

        # Get information of the current talk
        speaker = utils.get_speaker(talk)
        title = utils.get_title(talk)
        talk_id = utils.get_id(talk)

        # If the speaker is not in the dict, add the speaker with an empty list to store the talks in
        if speaker not in speaker_to_talks:
            speaker_to_talks[speaker] = []

        # Create a tuple with information of the current talk and add to the dict
        talk_info = (title, talk_id)
        speaker_to_talks[speaker].append(talk_info)

    # Create dict for speaker with multiple (more than one) talks
    speaker_to_multiple_talks = {}

    # Loop over the items of the speaker_to_talks dictionary
    for speaker, num_talks in speaker_to_talks.items():
        if len(num_talks) > 1:  # Check if speaker had multiple talks
            # If the speaker had more than one talk, add to the dict
            speaker_to_multiple_talks[speaker] = num_talks

    # Return dict of the speakers with multiple talks
    return speaker_to_multiple_talks


if __name__ == "__main__":
    path = '../Data/ted-talks/FILTERED_xml/ted_en.xml'
    root = utils.load_root(path)
    talks = utils.get_talks(root)

    n_talks = len(talks)

    titles_list_longest, ids_list_longest, wc_longest, mean_wc_longest = find_wc(talks, "longest")
    titles_list_shortest, ids_list_shortest, wc_shortest, mean_wc_shortest = find_wc(talks, "shortest")

    print(f'The total number of English Ted talks is: {n_talks}\n')

    print(f'Talk length: longest talk - {wc_longest} words, shortest talk - {wc_shortest} words\n'
          f'Longest talk: {titles_list_longest} (id: {ids_list_longest})\n'
          f'Shortest talk: {titles_list_shortest} (id: {ids_list_shortest})\n'
          f'Mean word count: {mean_wc_longest}\n')

    titles_oldest, ids_oldest = find_date(talks, "oldest")
    titles_newest, ids_newest = find_date(talks, "newest")
    print(f'Talk date:\n'
          f'Oldest talk: {titles_oldest} (id: {ids_oldest})\n'
          f'Newest talk: {titles_newest} (id: {ids_newest})\n')

    find_speaker_dict = find_speaker(talks)
    print(f'The speakers with more than one talk are the following:\n{find_speaker_dict}')
