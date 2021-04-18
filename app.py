
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, redirect
import mysql.connector

from secrets import mysql_host, password, database

mydb = mysql.connector.connect(
  host=mysql_host,
  user="root",
  password=password,
  database=database
)

mycursor = mydb.cursor()

sql = "INSERT INTO vaccine_posts (name, lat_lon, image) VALUES (%s, %s, %s)"
val = ("John", "34.213, -123.2352", "image url")
mycursor.execute(sql, val)

mydb.commit()


import os
SECRET_KEY = os.urandom(32)

app = Flask(__name__)


#client = MongoClient('', ssl=True,ssl_cert_reqs='CERT_NONE')
#mydb = client["smartcitizen"]
#mycol = mydb["zipCodes"]
#myquery = {"properties.GEOID10": "90040"}
#mydoc = mycol.find(myquery)

app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def home():
    #for x in mydoc:
    #    print(x)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vaccine_posts")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    return render_template(
        'index.html',
        title="Jinja Demo Site",
        description="Smarter page templates with Flask & Jinja."
    )

#@app.route("/zip-code")
#def getZipCodePolygon():
    #zipcode = db.zipCodes.find({"properties.GEOID10": "90040"})
    #print(zipcode)
    #return jsonify([todo for todo in zipcode])