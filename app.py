from flask import Flask, request, url_for, redirect, render_template, jsonify
from youtube_operations import get_audio_stream
from speech_to_text_api_operations import transcribe_audio
from transcription_operations import get_transcriptions
from detect_keywords import get_detections
from design_html import create_html


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/detect', methods=['POST'])
def detect():
    form_values = [x for x in request.form.values()]
    url, keywords = form_values[0], form_values[1].split(',')
    audio_segment_buffer = get_audio_stream(video_url=url)
    if type(audio_segment_buffer) == str:
        return render_template('home.html', display=audio_segment_buffer,
                               example='e.g. https://www.youtube.com/watch?v=vW9edcLqND0')

    response, time_offset = transcribe_audio(audio_data=audio_segment_buffer, language='en-US')
    transcription, timestamps_list = get_transcriptions(response_list=response, time_offset_list=time_offset)
    detections = get_detections(keywords=keywords, transcription=transcription, timestamps_list=timestamps_list)
    create_html(detections=detections)

    return render_template('output.html')


if __name__ == '__main__':
    app.run(debug=True)
