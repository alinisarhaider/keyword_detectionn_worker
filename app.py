from flask import Flask, request, url_for, redirect, render_template, jsonify
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


@app.route('/processing/')
def processing():
    query_id = request.args.get('job_id')
    if query_id:
        found_job = q.fetch_job(query_id)
        if found_job:
            status = 'failed' if found_job.is_failed else 'pending' if found_job.result is None else 'completed'
            if status == 'completed':
                return render_template('results.html')
        else:
            print('No job found!')
    return render_template('output.html')


@app.route('/detect', methods=['POST'])
def detect():
    form_values = [x for x in request.form.values()]
    url, keywords = form_values[0], form_values[1].split(',')
    job = q.enqueue(keyword_detection_processing, url, keywords, result_ttl=60)
    create_wait_html()

    return render_template('wait.html', job_id=job.id)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
