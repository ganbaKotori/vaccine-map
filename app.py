
from flask import Flask, render_template, request, jsonify, redirect

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from wtforms.validators import DataRequired

from werkzeug.utils import secure_filename
from upload_image import uploadImage
import mysql.connector
import json

from secrets import mysql_host, password, database

mydb = mysql.connector.connect(
  host=mysql_host,
  user="root",
  password=password,
  database=database
)

import os

mycursor = mydb.cursor()

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

app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def home():
    mycursor.execute("SELECT * FROM vaccine_posts")
    myresult = mycursor.fetchall()
    jsonString = json.dumps(myresult)
    print(jsonString)
    #for x in myresult:
    #    print(x)
    return render_template(
        'index.html',
        title="Vaccine Maps",
        description="Check a vaccine heat map",
        data=jsonString
    )

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
      name = request.form['name']
      lat = request.form['lat']
      lon = request.form['lon']
      print(name + " " + lat + " " + lon)

      f = request.files['file']
      f.save(secure_filename(f.filename))
      imageDownloadLink = uploadImage('./',secure_filename(f.filename))
      sql = "INSERT INTO vaccine_posts (name, lat, lon, image) VALUES (%s, %s, %s, %s)"
      val = (name, lat, lon, imageDownloadLink)
      mycursor.execute(sql, val)
      mydb.commit()

      mycursor.execute("SELECT * FROM vaccine_posts")
      myresult = mycursor.fetchall()
      return render_template('index.html',
            title="Vaccine Maps",
            description="Check a vaccine heat map",
            data=myresult
            )
    return render_template('upload.html')
  
if __name__ == '__main__':
    app.run()


