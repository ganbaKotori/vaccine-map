from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from wtforms.validators import DataRequired

import os

#Secret key is generated to be 32 randomized string characters
SECRET_KEY = os.urandom(32)

#secure session form with csrg protections
#csrf is a type of browser attack
class MyForm(FlaskForm):
    # member(field that is diplayed in your site)
    name = StringField('Enter Your Name', validators=[DataRequired()])
    file_upload = FileField('Upload Your File', validators=[FileRequired()])

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def home():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template(
        'index.html',
        title="Jinja Demo Site",
        description="Smarter page templates with Flask & Jinja.",
        form=form
    )
    
if __name__ == '__main__':
    app.run()