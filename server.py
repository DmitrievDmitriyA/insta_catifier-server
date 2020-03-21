import csv
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<string:page_name>.html')
def home(page_name=None):
    return render_template(f'{page_name}.html')

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(request)
        print (data)
        return redirect('processing.html')
    else:
        return 'something went wrong. try again'


#def write_to_file(data):
#    with open('database.txt', mode='a') as database:
#        email = data['email']
#        subject = data['subject']
#        message = data['message']
#        database.write(f'{email},{subject},{message}\n')
#
#def write_to_csv(data):
#    with open('database.csv', mode='a', newline='') as database:
#        email = data['email']
#        subject = data['subject']
#        message = data['message']
#        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#        csv_writer.writerow([email, subject, message])
#