from youtube_operations import get_audio_stream
from speech_to_text_api_operations import transcribe_audio
from transcription_operations import get_transcriptions
from detect_keywords import get_detections
from design_html import create_output_html, create_error_html


def keyword_detection_processing(url, keywords):
    print('Retrieving audio')
    audio_segment_buffer = get_audio_stream(video_url=url)
    if type(audio_segment_buffer) == str:
        create_error_html()
        return
    print('Retrieving transcriptions')
    response, time_offset = transcribe_audio(audio_data=audio_segment_buffer, language='en-US')
    transcription, timestamps_list = get_transcriptions(response_list=response, time_offset_list=time_offset)
    print('Formalising results')
    detections = get_detections(keywords=keywords, transcription=transcription, timestamps_list=timestamps_list)
    create_output_html(detections=detections)
    return
