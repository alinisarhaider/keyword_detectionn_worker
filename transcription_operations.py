def get_transcriptions(response_list: list, time_offset_list: list):
    transcription_list = list()
    timestamps_list = list()
    for response, time_offset in zip(response_list, time_offset_list):
        for result in response.results:
            alternative = result.alternatives[0]
            transcript = alternative.transcript
            timestamps = [time_offset + word_info.start_time.seconds +
                          word_info.start_time.nanos * 1e-9
                          for word_info in alternative.words]
            transcription_list.append(transcript)
            timestamps_list.extend(timestamps)

    transcription_temp = ' '.join(transcription_list)
    transcription = " ".join(transcription_temp.split())
    return transcription, timestamps_list
