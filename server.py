import time
import csv
from flask import Flask, render_template, request, redirect
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<string:page_name>.html')
def home(page_name=None):
    return render_template(f'{page_name}.html')


@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(request)
        print(data)
        return redirect('processing.html')
    else:
        return 'something went wrong. try again'


@app.route('/recognition_ready', methods=['GET'])
def recognition_ready():
    if request.method == 'GET':
        time.sleep(0.25)
        return '', 200
    else:
        return 'something went wrong. try again'


@app.route('/modification_ready', methods=['GET'])
def modification_ready():
    if request.method == 'GET':
        time.sleep(0.25)
        return '', 200
    else:
        return 'something went wrong. try again'


@app.route('/redirect_to_<string:page_name>', methods=['GET'])
def redirect_to(page_name=None):
    if request.method == 'GET':
        time.sleep(0.25)
        data = {'redirect': f'{page_name}.html'}
        return data, 200
    else:
        return 'something went wrong. try again'


@app.route('/get_photos', methods=['GET'])
def get_photos():
    if request.method == 'GET':

        photos = {str(key): './static/assets/cat-min.png' for key in range(10)}

        data = {'photos': photos}
        return data, 200
    else:
        return 'something went wrong. try again'
