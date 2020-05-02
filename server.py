import sys, os, time, datetime, json
sys.path.append(os.path.abspath('.\\backend'))
import backend.enhancementAdapter as enhancementAdapter
import backend.scrapingAdapter as scrapingAdapter
import backend.dataBaseAdapter as dataBaseAdapter
from cachetools import cached, TTLCache
from threading import RLock
from flask import Flask, render_template, request, redirect, url_for
import serverHelper


lock = RLock()


class ExtendedTTLCache(TTLCache):
    def popitem(self):
        key, value = super().popitem()
        print(datetime.datetime.now())
        with lock:
            #TODO: should be fixed
            #enhancementAdapter.removeResults(key)
            print('Removed results')
        return key, value


flask_app = Flask(__name__)
cache = ExtendedTTLCache(maxsize=100, ttl=60)  # ttl - time to live in seconds


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


@flask_app.route('/scraping_ready')
def recognition_ready():
    instagramAccount = request.args.get('instagramAccount')
    scrapingAdapter.scrapePhotos(instagramAccount)
    return '', 200


@flask_app.route('/modification_ready')
def modification_ready():
    instagramAccount = request.args.get('instagramAccount')
    enhancementAdapter.add_cats(instagramAccount)
    return '', 200


@flask_app.route('/redirect_to_gallery')
def redirect_to_gallery():
    time.sleep(1)
    instagramAccount = request.args.get('instagramAccount')
    data = {'redirect': url_for('gallery', instagramAccount=instagramAccount)}
    return data, 200 


@flask_app.route('/gallery.html')
def gallery():
    instagramAccount = request.args.get('instagramAccount')
    return render_template('gallery.html', instagramAccount=instagramAccount)


@flask_app.route('/get_photos')
def get_photos():
    instagramAccount = request.args.get('instagramAccount')
    data = dataBaseAdapter.get_results_from_bucket(instagramAccount)
    print(data)
    return data, 200


@flask_app.route('/redirect_to_<string:page_name>')
def redirect_to(page_name=None):
    time.sleep(1)
    data = {'redirect': f'{page_name}.html'}
    return data, 200