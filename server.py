import sys
import time
import serverHelper
from flask import Flask, render_template, request, redirect, url_for


flask_app = Flask(__name__)


# falsk uses GET request for every page by default, so there is no need to use it
# explicitly
@flask_app.route('/')
def index():
    return render_template('index.html')


@flask_app.route('/<string:page_name>.html')
def home(page_name=None):
    return render_template(f'{page_name}.html')


@flask_app.route('/submit_form')
def submit_form():
    if (instagramAccount:= request.args.get('instagramAccount')):
        if not serverHelper.validateInstagramAccount(instagramAccount):
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))

    if (userEmail:= request.args.get('userEmail')):
        if serverHelper.validateEmail(userEmail):
            # <-- create a task to process passed instagram account here
            return redirect(url_for('result', userEmail=userEmail))
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('processing', instagramAccount=instagramAccount))


@flask_app.route('/processing.html')
def processing():
    instagramAccount = request.args.get('instagramAccount')
    return render_template('processing.html', instagramAccount=instagramAccount)


@flask_app.route('/recognition_ready')
def recognition_ready():
    instagramAccount = request.args.get('instagramAccount')
    time.sleep(0.25)
    return '', 200


@flask_app.route('/modification_ready')
def modification_ready():
    time.sleep(0.25)
    return '', 200


@flask_app.route('/redirect_to_<string:page_name>')
def redirect_to(page_name=None):
    time.sleep(0.25)
    data = {'redirect': f'{page_name}.html'}
    return data, 200


@flask_app.route('/get_photos')
def get_photos():
    photos = {str(key): './static/assets/cat-min.png' for key in range(10)}
    data = {'photos': photos}
    return data, 200
