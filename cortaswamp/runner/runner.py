from celery import Celery
import subprocess

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def call_task():
    MyOut = subprocess.Popen(['locust', '-f', 'swamp.py', '--no-web', '-c', '10', '-r', '2', '--run-time', '1m', '--csv=example', '--host=https://www.inmar.com', '--port=8088'], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT)
    stdout,stderr = MyOut.communicate()
    print(stdout)
    print(stderr)