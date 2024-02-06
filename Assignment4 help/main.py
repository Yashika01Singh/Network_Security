from flask import Flask, render_template, send_file, url_for, request,flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import datetime
import pytz

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])
def home():
 
    # file = request.files['file']
    # print("file is", file)
    # print(type(file))
    # content = file.read()
    # # Get the current UTC time
    # utc_now = datetime.datetime.utcnow()
    # gmt = pytz.timezone('GMT')
    # gmt_now = utc_now.replace(tzinfo=pytz.utc).astimezone(gmt)
    # uploadedTime = f"The upload time is: {gmt_now.strftime('%Y-%m-%d %H:%M:%S')}"
    # content = content.decode('utf-8')
    # content = content + "\n" + uploadedTime
    # print(content)
    # file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
    # f = open(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)),'w')
    # f.write(content)
    # f.close() 
    return render_template('index.html')

@app.route('/download',methods=['GET', 'POST'])
def download_file():
    name = request.form['name']
    roll = request.form['roll']
    fileName = name + "_" + roll + ".txt"
    filename = 'static/files/' + fileName
    try:
        return send_file(filename, as_attachment=True)
    except:
        return "Not issued yet!"


if __name__ == '__main__':
    app.run(debug=True)