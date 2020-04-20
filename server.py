import sys, os, time, json, logging
sys.path.append(os.path.abspath('.\\backend'))
import backend.enhancementAdapter as enhancementAdapter
import backend.scrapingAdapter as scrapingAdapter
import backend.dataBaseAdapter as dataBaseAdapter
from flask import Flask, render_template, request, redirect, url_for
from flask_script import Manager
import serverHelper
from cache import ExtendedLFUCache

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
#from dramatiq.results.backends import RedisBackend
#from dramatiq.results import Results


#result_backend = RedisBackend()
broker = RabbitmqBroker()
#broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)


# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create cache
cache = ExtendedLFUCache(maxsize=10)


# Create Flask app and app manager
flask_app = Flask(__name__)
manager = Manager(flask_app)


@dramatiq.actor
def hello_world():
    # response = requests.get(url)
    # count = len(response.text.split(" "))
    print('Hello world!')
    time.sleep(4.25)


# Server initialization
@manager.command
def runserver():
    # let's initialize cache first with database content
    accounts = dataBaseAdapter.get_accounts_from_bucket()
    print(accounts)
    for account in accounts:
        data = dataBaseAdapter.get_results_from_bucket(account)
        cache[account] = data

    logger.info('cache is initialized: ' + key for key, value in cache)

    flask_app.run()


# === Home page ===


# falsk uses GET request for every page by default, so there is no need to use it
# explicitly
@flask_app.route('/')
@flask_app.route('/index.html')
def index():
    return render_template('index.html')


@flask_app.route('/submit_form')
def submit_form():
    if (instagramAccount:= request.args.get('instagramAccount')):
        if not serverHelper.validateInstagramAccount(instagramAccount):
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))

    if (userEmail:= request.args.get('userEmail')):
        if serverHelper.validateEmail(userEmail):
            return redirect(url_for('result', userEmail=userEmail))
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('processing', instagramAccount=instagramAccount))


# === A generic stub for orphan pages ===


@flask_app.route('/<string:page_name>.html')
def generic(page_name=None):
    return render_template(f'{page_name}.html')


@flask_app.route('/redirect_to_<string:page_name>')
def redirect_to(page_name=None):
    time.sleep(1)
    data = {'redirect': f'{page_name}.html'}
    return data, 200


# === Processing page ===


@flask_app.route('/processing.html')
def processing():
    instagramAccount = request.args.get('instagramAccount')
    return render_template('processing.html', instagramAccount=instagramAccount)


@flask_app.route('/scraping_ready')
def recognition_ready():
    instagramAccount = request.args.get('instagramAccount')
    message = hello_world.send()
    time.sleep(0.25)
    message.get_result(block=True)
    print('Yes!')
    if instagramAccount in cache:
            return '', 200

    scrapingAdapter.scrapePhotos(instagramAccount)
    return '', 200


@flask_app.route('/modification_ready')
def modification_ready():
    instagramAccount = request.args.get('instagramAccount')
    if instagramAccount in cache:
        return '', 200

    enhancementAdapter.add_cats(instagramAccount)
    return '', 200


@flask_app.route('/redirect_to_gallery')
def redirect_to_gallery():
    time.sleep(1)
    instagramAccount = request.args.get('instagramAccount')
    data = {'redirect': url_for('gallery', instagramAccount=instagramAccount)}
    return data, 200 


# === Gallery page ===


@flask_app.route('/gallery.html')
def gallery():
    instagramAccount = request.args.get('instagramAccount')
    return render_template('gallery.html', instagramAccount=instagramAccount)


@flask_app.route('/get_photos')
def get_photos():
    instagramAccount = request.args.get('instagramAccount')

    if instagramAccount in cache:
        data = cache[instagramAccount]
        return data, 200

    data = dataBaseAdapter.get_results_from_bucket(instagramAccount)
    cache[instagramAccount] = data
    return data, 200


if __name__ == "__main__":
    manager.run()