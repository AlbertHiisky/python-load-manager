# existence is pain
from flask import Flask
import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.app_active_requests = 0


@app.route('/')
def sample():
    app.app_active_requests += 1
    return "Got request"


@app.route('/healthcheck')
def healthcheck():
    return "OK"


@app.route('/loaded')
def loaded():
    return str(app.app_active_requests)
    
@app.route('/dumptxt')
def dumptxt():
    with open("log.txt", "r") as fo:
        all_of_it = fo.read()
    return all_of_it


def log_in_file():
    with open("log.txt", "a") as fo:
        fo.write('{}: {}\n'.format(datetime.datetime.now(), str(app.app_active_requests)))


def process_request():
    if app.app_active_requests > 0:
        app.app_active_requests -= 1


sched = BackgroundScheduler(daemon=True)
sched.add_job(log_in_file, 'interval', seconds=10)
# sched.add_job(process_request, 'interval', seconds=5)
sched.start()
atexit.register(lambda: sched.shutdown())


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
