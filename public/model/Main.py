from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_cors import CORS
from datetime import datetime
import cv2 as cv
import random
import string
import os
import numpy
import pandas as pd
import matplotlib.image as mpimg
import importlib
import matplotlib.image as mpimg 
from Trainbase import Trainbase, TrainModel
from PIL import Image
from Preprobase import Preprobase
from flask_mysqldb import MySQL
from io import StringIO
import base64

app = Flask(__name__, static_url_path='')
app.secret_key = "hXFmjiul8hmiFm5Yk66fAecCF02q4PWYpiOcc2GbCh8GX2jQm5lW65w33W5MNL50"
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pengenalanpola'
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    train = Trainbase()
except Exception as e:
    train = []

prepro = Preprobase()
mysql = MySQL(app)


def exQuery(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    rv = cur.fetchall()
    cur.close()
    return rv

def getFileData():
    f = open(basePath+"/model/trainFileHandling.txt", "r")
    try:
        num_clases = int(f.read())
    except Exception as e:
        num_clases = 0
    f.close()
    return num_clases
def setFileData(num_clases):
    f = open(basePath+"/model/trainFileHandling.txt", "wt")
    f.write(str(num_clases))
    f.close()
    return True

@app.route("/train", methods=['GET'])
def trainModel():
    model = TrainModel()
    return model.createModel(basePath+'/model/pictures/')

@app.route("/students", methods=['POST'])
def inputTaskApi():
    data = request.form
    name = data['name']
    picture = data['picture'].replace('data:image/jpeg;base64,', '')
    imgBase64 = picture.replace(' ','+')
    token = data['npm']
    now = datetime.now()
    curTime = now.strftime("%Y-%m-%d %H:%M:%S")
    extension = '.jpg'
    filename = token + extension
    realPath = basePath + '/model/pictures/' + token
    imagePath = basePath + '/model/realPict/' + filename
    if not os.path.exists(realPath):
        os.makedirs(realPath,mode=0o777)
        os.chmod(realPath,0o777)

    original_image = cv.imdecode(numpy.fromstring(base64.b64decode(imgBase64), numpy.uint8), cv.IMREAD_UNCHANGED)
    detectedFace = prepro.drawRealpictContour(original_image,imagePath)
    os.chmod(imagePath,0o777)
    imageName = realPath+'/'+token
    img = cv.imdecode(numpy.fromstring(base64.b64decode(imgBase64), numpy.uint8), cv.IMREAD_UNCHANGED)
    if(prepro.detectCropResize(imageName,img,224,detectedFace)):
        num_clases = getFileData()
        num_clases += 1
        if(setFileData(num_clases)):
            exQuery("INSERT INTO students(name, npm, created_at, updated_at) VALUES ('"+name+"','"+token+"', '"+curTime+"', '"+curTime+"')")
            return jsonify({'msg': 'Berhasil','color':'#32bdca'})
        else:
            return jsonify({'msg': 'Gagal','color':'#d32f2f'})
    return jsonify({'msg': 'Gagal','color':'#d32f2f'})
    

@app.route("/verify", methods=['POST'])
def verify():
    data = request.form
    picture = data['picture'].replace('data:image/jpeg;base64,', '')
    imgBase64 = picture.replace(' ','+')
    now = datetime.now()
    curTime = now.strftime("%Y-%m-%d %H:%M:%S")
    original_image = cv.imdecode(numpy.fromstring(base64.b64decode(imgBase64), numpy.uint8), cv.IMREAD_UNCHANGED)
    reshapeImg = prepro.cropresize(original_image)
    (ynew, train_labels, score) = train.verif(reshapeImg)
    if(len(score) > 0):
        if(score[0][ynew] > 0.95):
            rv = exQuery("SELECT name, id FROM students WHERE npm = '"+train_labels[ynew]+"'")
            # exQuery("INSERT INTO attendance(student_id, created_at, updated_at) VALUES ('"+name+"', '"+curTime+"', '"+curTime+"')")
            return jsonify({'msg': str(rv[0][0]), 'npm': train_labels[ynew],'index': str(ynew), 'score': str(score[0][ynew])})
        else:
            return jsonify({'msg': 'Wajah tidak dikenali', 'score': str(score[0][ynew])})
    return jsonify({'msg': 'Gagal'})
    

@app.route("/", methods=['GET'])
def getTask():
    # rv = exQuery("SELECT * FROM students")
    # return jsonify({'msg': str(rv)})
    return jsonify({'msg': str(cv.__version__)})

if __name__ == '__main__':
    app.debug = True
    app.run(host= '192.168.100.136')