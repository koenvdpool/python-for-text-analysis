import glob
import utils


def map_languages_to_paths(folder_path, /):
    """
    This function creates a dictionary of languages mapped to XML file paths.

    :param folder_path: the pathname to the XML folder
    :return: a dict with the language-to-filepath mapping
    """
    # Create a dict for the language-to-XML file path mapping
    lang_to_paths = {}

    # Loop over all files in the folder that begin with 'ted_' and end with '.xml'
    for xml_filepath in glob.glob(f"{folder_path}/ted_*.xml"):
        filename = xml_filepath.split('/')[-1]
        lang = filename.split('_')[1].split('.')[0]  # Extract language from the filename
        lang_to_paths[lang] = xml_filepath  # Add mapping of the language-to-XML file path to the dict

    return lang_to_paths


def find_coverage(dict_lang_to_path, n_translations, /):
    """
    Finds the languages with either the least or most translations.

    :param dict_lang_to_path: a dict with the language-to-filepath mapping
    :param n_translations: defines if you want the language with the 'most' or 'least' translation
    :return: a dict mapping the language(s) to their corresponding translation count
    """
    # Create dict to map the language to their corresponding translation count
    lang_to_n_talks = {}

    for lang, filepath in dict_lang_to_path.items():
        if lang != "en":  # Skip the original talks in English
            root = utils.load_root(filepath)
            # Access the talks in each file, count them, and add to the dict
            talks = utils.get_talks(root)
            n_talks = len(talks)
            lang_to_n_talks[lang] = n_talks

    # Create a new dict to store the selected languages and their number of talks in
    selected_lang_to_n_talks = {}

    for lang, n_talks in lang_to_n_talks.items():
        if n_translations == 'most':
            # Look for the number of the most translations
            most_n_translations = max(lang_to_n_talks.values())
            # Check if the current language has the most translations, if yes, add to dict
            if n_talks == most_n_translations:
                selected_lang_to_n_talks[lang] = n_talks

        elif n_translations == 'least':
            # Look for the number of the least translations
            least_n_translations = min(lang_to_n_talks.values())
            # Check if the current language has the least translations, if yes, add to dict
            if n_talks == least_n_translations:
                selected_lang_to_n_talks[lang] = n_talks

    return selected_lang_to_n_talks


def get_id_title_dict(path, /):
    """
    Maps the talk ID to the English title.

    :param path: file path to XML file
    :return: a dict with a ID-to-title mapping
    """

    # Create dict for ID-to-title mapping
    id_to_title = {}

    # Access the root and talks in the file
    root = utils.load_root(path)
    talks = utils.get_talks(root)

    # Loop over the talks
    for talk in talks:
        # Get the ID and title and add to the dict
        talk_id = utils.get_id(talk)
        title = utils.get_title(talk)
        id_to_title[talk_id] = title

    return id_to_title


def map_talks_to_languages(dict_lang_to_path, /):
    """
    Maps the talk IDs to the languages into which the talks are translated.

    :param dict_lang_to_path: a dict with the language-to-filepath mapping
    :return: a dict with a ID-to-language mapping
    """
    # Create a dict for the ID-to-language mapping
    talk_id_to_lang = {}

    for lang, filepath in dict_lang_to_path.items():
        if lang != "en":  # Skip the original talks in English
            # Access the root and talks in the file
            root = utils.load_root(filepath)
            talks = utils.get_talks(root)
            for talk in talks:
                talk_id = utils.get_id(talk)  # Get talk ID
                # If talk ID not yet in dict, add with an empty list for the languages
                if talk_id not in talk_id_to_lang:
                    talk_id_to_lang[talk_id] = []
                # Add ID-to-language mapping to the dict
                talk_id_to_lang[talk_id].append(lang)

    return talk_id_to_lang


def map_nlang_to_talks(talk_id_to_lang, /):
    """
    Maps the number of translations to their corresponding talk IDs.

    :param talk_id_to_lang: a dict with a ID-to-language mapping
    :return: a number of translations to talk IDs mapping
    """
    # Create a dictionary mapping translation counts to talk IDs.
    nlang_to_talk_ids = {}

    for talk_id, list_of_lang in talk_id_to_lang.items():
        # Get number of translations for each talk
        n_translations = len(list_of_lang)
        # Add empty list for talk IDs if translation count is not in the dictionary
        if n_translations not in nlang_to_talk_ids:
            nlang_to_talk_ids[n_translations] = []
        # Add number of translations to talk ID mapping to the dict
        nlang_to_talk_ids[n_translations].append(talk_id)

    return nlang_to_talk_ids


def find_top_coverage(dict_lang_to_path, n_translations, /):
    """
    Finds either the most or least translated talk.

    :param dict_lang_to_path: a dict with the language-to-filepath mapping
    :param n_translations: specifies whether to find the talk with the 'most' or 'least' translations
    :return: dict with a title-to-language mapping
    """
    # Get ID to title mapping of the original English talks
    en_filepath = dict_lang_to_path.get('en')
    en_id_to_title = get_id_title_dict(en_filepath)

    # Get ID to languages mapping
    talk_id_to_lang = map_talks_to_languages(dict_lang_to_path)

    # Get translations count to ID mapping
    nlang_to_talk_id = map_nlang_to_talks(talk_id_to_lang)

    # Create dict for the selected talks to translations mapping
    selected_talk_to_translations = {}

    if n_translations == 'most':
        # Get the max number of translations
        max_nlang = max(nlang_to_talk_id.keys())
        # Get the IDs of the talks with the max number of translations
        list_id_most_translations = nlang_to_talk_id.get(max_nlang)
        for talk_id in list_id_most_translations:
            if talk_id in en_id_to_title:  # Make sure it is a translation from an English talk
                # Get title and languages, then add to dict
                title = en_id_to_title.get(talk_id)
                languages = talk_id_to_lang.get(talk_id)
                selected_talk_to_translations[title] = languages

    elif n_translations == 'least':
        # Get the min number of translations
        min_nlang = min(nlang_to_talk_id.keys())
        # Get the IDs of the talks with the min number of translations
        list_id_least_translations = nlang_to_talk_id.get(min_nlang)
        for talk_id in list_id_least_translations:
            if talk_id in en_id_to_title:  # Make sure it is a translation from an English talk
                # Get title and languages, then add to dict
                title = en_id_to_title.get(talk_id)
                languages = talk_id_to_lang.get(talk_id)
                selected_talk_to_translations[title] = languages

    return selected_talk_to_translations


if __name__ == "__main__":

    print("STEP 1 - Map languages to filepaths:")
    xml_folder_path = "../Data/ted-talks/FILTERED_xml"
    dict_lang_to_xml_paths = map_languages_to_paths(xml_folder_path)
    print(dict_lang_to_xml_paths)
    print()

    print("STEP 2 - most/least translations:")
    lang_most_translations = find_coverage(dict_lang_to_xml_paths, "most")
    lang_least_translations = find_coverage(dict_lang_to_xml_paths, "least")
    print(f'The dictionary with the language(s) with the most translations:\n{lang_most_translations}')
    print(f'The dictionary with the language(s) with the least translations:\n{lang_least_translations}')
    print()

    print("STEP 3 - Map talk ids to titles:")
    path_en = '../Data/ted-talks/FILTERED_xml/ted_en.xml'
    dict_en_id_to_title = get_id_title_dict(path_en)
    print(dict_en_id_to_title)
    print()

    print("STEP 4 - Map talks to languages they have been translated into:")
    dict_id_to_lang = map_talks_to_languages(dict_lang_to_xml_paths)
    print(dict_id_to_lang)
    print()

    print("STEP 5 - Map number of languages to talk:")
    dict_nlang_to_talks = map_nlang_to_talks(dict_id_to_lang)
    print(dict_nlang_to_talks)
    print()

    print("STEP 6 - Put it all together:")
    most_translated_talks = find_top_coverage(dict_lang_to_xml_paths, 'most')
    least_translated_talks = find_top_coverage(dict_lang_to_xml_paths, 'least')
    print(f'The most translated talk(s) are/is:\n{most_translated_talks}')
    print(f'The least translated talk(s) are/is:\n{least_translated_talks}')
