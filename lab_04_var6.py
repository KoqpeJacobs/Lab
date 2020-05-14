# py_ver == "3.6.9"
import flask
import cgi
import subprocess


app = flask.Flask(__name__)


import requests
# check internet connection is available
inet_conn = False
if requests.__version__ <= '2.19.1':
    try:
        requests.get('https://google.com')
        inet_conn = True
    except:
        pass


import json
import time


@app.route('/feedback_form')
def introduction():
    feedback = ''
    with open('feedback.json', 'r') as feedback_file:
        feedback_dict = json.loads(feedback_file.read().decode("utf-8"))
        for key, value in feedback_dict.items():
            feedback += "<p><i>Анононим, %s</i>: %s</p>" % (key, value)
    return """<html>
                <title>Обратная связь</title>
                <body>
                %s
                    <form action="/save_feedback" method="post">
                        Поделитесь своим мнением: <input name="feedback" type="text" />
                        <input name="submit" type="submit" value="Отправить">
                    </form>
                </body>
            </html>
""" % feedback


@app.route('/save_feedback', methods=["GET", "POST"])
def index_page():
    feedback = flask.request.form.get('feedback')
    feedback_dict = {}
    with open('feedback.json', 'r') as feedback_file:
        feedback_dict.update(json.loads(feedback_file.read().decode("utf-8")))
    feedback_dict[time.time()] = feedback
    with open('feedback.json', 'w') as feedback_file:
        feedback_file.write(json.dumps(feedback_dict).encode("utf-8"))
    return flask.redirect('/feedback_form')


@app.route('/send_host')
def set_target():
    return """
            <html>
                <title>Target selection</title>
                <body>
                    <form action="/scan">
                        Enter target IP: <input name="ip" type="text" />
                        <input name="submit" type="submit">
                    </form>
                </body>
            </html>
"""


import os


@app.route('/scan')
def scanner():
    ip = cgi.escape(flask.request.args.get('ip'))
    result = subprocess.call(["nmap", ip], shell=True)
    return "%s" % result


@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Content-Security-Policy'] = "default-src 'self'"
    return response


if __name__ == '__main__':
    app.run()
