
from flask import Flask, render_template, request

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from wtforms.validators import DataRequired

from werkzeug.utils import secure_filename

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

#Secret key is generated to be 32 randomized string characters
SECRET_KEY = os.urandom(32)

#secure session form with csrg protections
#csrf is a type of browser attack
class MyForm(FlaskForm):
    # member(field that is diplayed in your site)
    file_upload = FileField('Upload Your File', validators=[FileRequired()])
    name = StringField('Enter Your Name', validators=[DataRequired()])

class Photo(FlaskForm):
    file_upload = FileField('Upload Your File', validators=[FileRequired()])
    name = StringField('Enter Your Name', validators=[DataRequired()])

app = Flask(__name__)


#client = MongoClient('', ssl=True,ssl_cert_reqs='CERT_NONE')
#mydb = client["smartcitizen"]
#mycol = mydb["zipCodes"]
#myquery = {"properties.GEOID10": "90040"}
#mydoc = mycol.find(myquery)

app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def home():
    #form = MyForm()
    #if form.validate_on_submit():
    #    return redirect('/success')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vaccine_posts")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    return render_template(
        'index.html',
        title="Vaccine Maps",
        description="Check a vaccine heat map"
    )
 
#@app.route("/zip-code")
#def getZipCodePolygon():
    #zipcode = db.zipCodes.find({"properties.GEOID10": "90040"})
    #print(zipcode)
    #return jsonify([todo for todo in zipcode])

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      #return 'file uploaded successfully'
      return render_template('index.html',
              title="Vaccine Maps",
        description="Check a vaccine heat map")
    return render_template('upload.html')
  
if __name__ == '__main__':
    app.run()

