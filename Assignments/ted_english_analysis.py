import utils


def find_wc(talk_elements, /, length="longest"):
    """

    """
    selected_word_count = 0
    selected_talks = []
    all_word_counts = []

    for talk in talk_elements:
        current_word_count = utils.get_word_count(talk)
        if current_word_count <= 0:
            continue

        all_word_counts.append(current_word_count)
        if length == "longest":
            if current_word_count > selected_word_count:
                selected_word_count = current_word_count
                selected_talks = [talk]
            elif current_word_count == selected_word_count:
                selected_talks.append(talk)

        elif length == "shortest":
            if (selected_word_count == 0) or (current_word_count < selected_word_count):
                selected_word_count = current_word_count
                selected_talks = [talk]
            elif current_word_count == selected_word_count:
                selected_talks.append(talk)

    selected_titles = []
    selected_ids = []
    mean_word_count = utils.get_mean_word_count(all_word_counts)

    for talk in selected_talks:
        title = utils.get_title(talk)
        selected_titles.append(title)
        talk_id = utils.get_id(talk)
        selected_ids.append(talk_id)

    return selected_titles, selected_ids, selected_word_count, mean_word_count


def find_date(talk_elements, /, time="oldest"):
    """

    """

    selected_talks = []
    selected_date = ''

    for talk in talk_elements:

        word_count = utils.get_word_count(talk)
        if word_count <= 0:
            continue

        current_date = utils.get_date(talk)
        if current_date != "No date available":
            if not selected_talks:
                selected_talks = [talk]
                selected_date = current_date
            else:
                dates_comparison = utils.compare_dates(selected_date, current_date)
                if time == "newest":
                    if dates_comparison == 'newer':
                        selected_talks = [talk]
                        selected_date = current_date
                    elif dates_comparison == 'same':
                        selected_talks.append(talk)

                if time == "oldest":
                    if dates_comparison == 'older':
                        selected_talks = [talk]
                        selected_date = current_date
                    elif dates_comparison == 'same':
                        selected_talks.append(talk)

    selected_titles = []
    selected_ids = []

    for talk in selected_talks:
        title = utils.get_title(talk)
        selected_titles.append(title)
        talk_id = utils.get_id(talk)
        selected_ids.append(talk_id)

    return selected_titles, selected_ids


def find_speaker(talk_elements, /):
    """

    """
    speaker_to_talks = {}

    for talk in talk_elements:
        word_count = utils.get_word_count(talk)
        if word_count <= 0:
            continue

        speaker = utils.get_speaker(talk)
        title = utils.get_title(talk)
        talk_id = utils.get_id(talk)

        if speaker not in speaker_to_talks:
            speaker_to_talks[speaker] = []

        talk_info = (title, talk_id)
        speaker_to_talks[speaker].append(talk_info)

    speaker_to_multiple_talks = {}

    for speaker, num_talks in speaker_to_talks.items():
        if len(num_talks) > 1:
            speaker_to_multiple_talks[speaker] = num_talks

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

