from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

import os

#Secret key is generated to be 32 randomized string characters
SECRET_KEY = os.urandom(32)

#secure session form with csrg protections
#csrf is a type of browser attack
class MyForm(FlaskForm):
    # member(field that is diplayed in your site)
    name = StringField('Enter Your Name', validators=[DataRequired()])

class Photo(FlaskForm):
    file_upload = FileField('Upload Your File', validators=[FileRequired()])
    name = StringField('Enter Your Name', validators=[DataRequired()])

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def home():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template(
        'index.html',
        title="Vaccine Maps",
        description="Check a vaccine heat map",
        form=form
    )
    

@app.route('/upload')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file1():
    if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'
  
if __name__ == '__main__':
    app.run()