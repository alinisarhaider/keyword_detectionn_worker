from flask import Flask, request, url_for, redirect, render_template, render_template_string
from background_worker import keyword_detection_processing
import os
from rq import Queue
from rq.job import Job
from worker import conn
from design_html import create_results_html, create_error_html


app = Flask(__name__)
q = Queue(connection=conn)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/processing/')
def processing():
    query_id = request.args.get('job')
    if query_id:
        found_job = q.fetch_job(query_id)
        if found_job:
            # print('tada!', found_job.is_failed)
            # job = Job.fetch(query_id, connection=conn)
            # status_ = job.get_status()
            # print(status_)
            status = 'failed' if found_job.is_failed else 'pending' if found_job.result is None else 'completed'
            if status == 'completed':
                if type(found_job.result) == str:
                    error_data = create_error_html(found_job.result)
                    return render_template_string(error_data)
                else:
                    data = create_results_html(detections=found_job.result)
                    return render_template_string(data)
        else:
            error_data = create_error_html('Process failed because of limited server memory. Please try again.')
            return render_template_string(error_data)
    return render_template('process.html', job_id=query_id)


@app.route('/detect', methods=['POST'])
def detect():
    form_values = [x for x in request.form.values()]
    url, keywords = form_values[0], form_values[1].split(',')
    job = q.enqueue(keyword_detection_processing, url, keywords, result_ttl=27, job_timeout=600)

    return render_template('wait.html', job_id=job.id)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
