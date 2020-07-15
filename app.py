from flask import Flask, request, url_for, redirect, render_template
from design_html import create_wait_html
from background_worker import keyword_detection_processing
import os
from rq import Queue
from worker import conn


app = Flask(__name__)
q = Queue(connection=conn)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/processing')
def processing():
    return render_template('output.html')


@app.route('/detect', methods=['POST'])
def detect():
    form_values = [x for x in request.form.values()]
    url, keywords = form_values[0], form_values[1].split(',')
    q.enqueue(keyword_detection_processing, url, keywords, result_ttl=60)
    create_wait_html()

    return render_template('wait.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
