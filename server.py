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
        print (data)
        return redirect('processing.html')
    else:
        return 'something went wrong. try again'

@app.route('/recognition_ready', methods=['GET'])
def recognition_ready():
    if request.method == 'GET':
        time.sleep(1.0)
        return '', 200
    else:
        return 'something went wrong. try again'

@app.route('/modification_ready', methods=['GET'])
def modification_ready():
    if request.method == 'GET':
        time.sleep(1.0)
        return '', 200
    else:
        return 'something went wrong. try again'

@app.route('/redirect_to_index', methods=['GET'])
def redirect_to_index():
    if request.method == 'GET':
        time.sleep(1.0)
        data = {'redirect': '/index.html'}
        return data, 200
    else:
        return 'something went wrong. try again'