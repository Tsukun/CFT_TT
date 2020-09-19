from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import numpy as np
import librosa
import librosa.display
import os
import matplotlib.pyplot as plt
from io import BytesIO
import base64

UPLOAD_FOLDER = '/home/tsukune/Desktop/project/python_project/mp3_file'
ALLOWED_EXTENSIONS = set(['mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/mp3_file/<filename>')

def uploaded_file(filename):
    fmp3 = send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    y, sr = librosa.load("/home/tsukune/Desktop/project/python_project/mp3_file/" + filename)
    fig, ax = plt.subplots(nrows = 1, ncols = 1, sharex = True)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref = np.max)
    img = librosa.display.specshow(D, y_axis = 'linear', x_axis = 'time', sr = sr, ax = ax)
    buf = BytesIO()
    fig.savefig(buf, format = 'png')
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    return f"<img src = 'data:image/png; base64, {data}' style=\"display:block; margin-left:auto; margin-right:auto\">"

