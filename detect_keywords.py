import re


def get_detections(keywords: list, transcription: str, timestamps_list):
    occurrence_details = dict()
    for keyword in keywords:
        # Search for all the occurrences of a keyword and store it's first letter index.
        word_index = [word.start() for word in re.finditer(keyword, transcription)]
        # 1 --> Get the location of the word in the whole text using word_index
        # 2 --> With the help of location, map it to the corresponding timestamp
        # 3 --> Repeat for all occurrences and store it in a dictionary with the keyword
        occurrence_details[keyword] = [timestamps_list[len(transcription[:current_index].split(' ')) - 1]
                                       for current_index in word_index]
    return occurrence_details
