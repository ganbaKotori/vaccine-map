from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

import os
SECRET_KEY = os.urandom(32)

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

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