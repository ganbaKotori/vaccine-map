
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_pymongo import PyMongo

from pymongo import MongoClient

from flask import Flask, render_template, jsonify, redirect

import os
SECRET_KEY = os.urandom(32)
UPLOAD_FOLDER = 'vaccine-map\photo-submission'

app = Flask(__name__)

client = MongoClient('', ssl=True,ssl_cert_reqs='CERT_NONE')

mydb = client["smartcitizen"]
mycol = mydb["zipCodes"]

myquery = {"properties.GEOID10": "90723"}

mydoc = mycol.find(myquery)

class MyForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])

app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    form = MyForm()
    for x in mydoc:
        print(x)
    if form.validate_on_submit():
        return redirect('/success')
    return render_template(
        'index.html',
        title="Jinja Demo Site",
        description="Smarter page templates with Flask & Jinja.",
        form=form
    )

#@app.route("/zip-code")
#def getZipCodePolygon():
    #zipcode = db.zipCodes.find({"properties.GEOID10": "90040"})
    #print(zipcode)
    #return jsonify([todo for todo in zipcode])