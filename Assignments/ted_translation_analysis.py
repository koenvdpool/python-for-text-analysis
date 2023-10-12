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
    Todo.
    :param dict_lang_to_path:
    :param n_translations:
    :return:
    """
    lang_to_n_talks = {}

    for lang, filepath in dict_lang_to_path.items():
        if lang != "en":
            root = utils.load_root(filepath)
            talks = utils.get_talks(root)
            n_talks = len(talks)
            lang_to_n_talks[lang] = n_talks

    selected_lang_to_n_talks = {}

    for lang, n_talks in lang_to_n_talks.items():

        if n_translations == 'most':
            most_n_translations = max(lang_to_n_talks.values())
            if n_talks == most_n_translations:
                selected_lang_to_n_talks[lang] = n_talks

        elif n_translations == 'least':
            least_n_translations = min(lang_to_n_talks.values())
            if n_talks == least_n_translations:
                selected_lang_to_n_talks[lang] = n_talks

    return selected_lang_to_n_talks


def get_id_title_dict(path, /):
    """

    """

    id_to_title = {}

    root = utils.load_root(path)
    talks = utils.get_talks(root)

    for talk in talks:
        talk_id = utils.get_id(talk)
        title = utils.get_title(talk)
        id_to_title[talk_id] = title

    return id_to_title


def map_talks_to_languages(dict_lang_to_path, /):
    """

    """
    talk_id_to_lang = {}

    for lang, filepath in dict_lang_to_path.items():
        if lang != "en":
            root = utils.load_root(filepath)
            talks = utils.get_talks(root)
            for talk in talks:
                talk_id = utils.get_id(talk)
                if talk_id not in talk_id_to_lang:
                    talk_id_to_lang[talk_id] = []
                talk_id_to_lang[talk_id].append(lang)

    return talk_id_to_lang


def map_nlang_to_talks(talk_id_to_lang, /):
    """

    """
    nlang_to_talk_ids = {}

    for talk_id, list_of_lang in talk_id_to_lang.items():
        n_translations = len(list_of_lang)
        if n_translations not in nlang_to_talk_ids:
            nlang_to_talk_ids[n_translations] = []
        nlang_to_talk_ids[n_translations].append(talk_id)

    return nlang_to_talk_ids


def find_top_coverage(dict_lang_to_path, n_translations, /):
    """

    """

    en_filepath = dict_lang_to_path.get('en')

    en_id_to_title = get_id_title_dict(en_filepath)

    talk_id_to_lang = map_talks_to_languages(dict_lang_to_path)
    nlang_to_talk_id = map_nlang_to_talks(talk_id_to_lang)

    max_nlang = max(nlang_to_talk_id.keys())
    min_nlang = min(nlang_to_talk_id.keys())

    list_id_most_translations = nlang_to_talk_id.get(max_nlang)
    list_id_least_translations = nlang_to_talk_id.get(min_nlang)

    selected_talk_to_translations = {}

    if n_translations == 'most':
        for talk_id in list_id_most_translations:
            if talk_id in en_id_to_title:
                title = en_id_to_title.get(talk_id)
                languages = talk_id_to_lang.get(talk_id)
                selected_talk_to_translations[title] = languages

    elif n_translations == 'least':
        for talk_id in list_id_least_translations:
            if talk_id in en_id_to_title:
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
