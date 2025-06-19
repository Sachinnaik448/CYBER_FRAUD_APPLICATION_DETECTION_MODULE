from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import classifier
import pickle
import numpy as np
import pandas as pd
import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/upload/'
app.config['SECRET_KEY'] = 'd3Y5d5nJkU6CdwY'
if os.path.exists(app.config['UPLOAD_FOLDER']):
    print("directory exists")
else:
    os.makedirs(app.config['UPLOAD_FOLDER'])
    print("directory created")


##Define the flask app


@app.route('/')
@app.route('/first')
def first():
    return render_template('first.html')
@app.route('/login')
def login():
    return render_template('login.html')
def home():
	return render_template('index.html')

 
@app.route('/upload')
def upload():
    return render_template('upload.html')  

@app.route('/preview',methods=["POST"])
def preview():
    if request.method == 'POST':
        dataset = request.files['datasetfile']
        df = pd.read_csv(dataset,encoding = 'unicode_escape')
        df.set_index('Id', inplace=True)
        return render_template("preview.html",df_view = df) 



@app.route("/home", methods=["GET", "POST"])
def home():
    algorithms = {'Neural Network': '92.26 %', 'Support Vector Classifier': '89 %'}
    result, accuracy, name, sdk, size = '', '', '', '', ''
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.apk'):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if request.form['algorithm'] == 'Neural Network':
                accuracy = algorithms['Neural Network']
                result, name, sdk, size = classifier.classify(os.path.join(app.config['UPLOAD_FOLDER'], filename), 0)
            elif request.form['algorithm'] == 'Support Vector Classifier':
                accuracy = algorithms['Support Vector Classifier']
                result, name, sdk, size = classifier.classify(os.path.join(app.config['UPLOAD_FOLDER'], filename), 1)
    return render_template("index.html", result=result, algorithms=algorithms.keys(), accuracy=accuracy, name=name,
                           sdk=sdk, size=size)









@app.route('/chart')
def chart():
    return render_template('chart.html')



if __name__ == '__main__':
	app.run(debug=True)