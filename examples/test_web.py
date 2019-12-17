#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 06:05:39 2017
@author: ubuntu
ref: https://towardsdatascience.com/build-face-recognition-as-a-rest-api-4c893a16446e
     https://flask-appbuilder.readthedocs.io/en/latest/quickfiles.html
     https://gist.github.com/liulixiang1988/cc3093b2d8cced6dcf38
"""

import os
from flask import Flask, request, redirect, url_for,jsonify,render_template
from werkzeug import secure_filename
#import json
import time
import cv2
import numpy as np
from os.path import exists#,isfile, join

app = Flask(__name__)#, static_folder='static', static_url_path='')

ALI_MODEL_PATH = "models/seeta_fa_v1.1.bin"
DET_MODEL_PATH = "models/seeta_fd_frontal_v1.0.bin"
REC_MODEL_PATH = "models/seeta_fr_v1.0.bin"

from pyseeta import Detector
from pyseeta import Aligner
from pyseeta import Identifier

UPLOAD_FOLDER = 'examples/uploads'
WEBFILE_FOLDER = 'webfiles'
app.detector = Detector(DET_MODEL_PATH)
app.aligner = Aligner(ALI_MODEL_PATH)
app.identifier = Identifier(REC_MODEL_PATH)

app.results = []
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['WEBFILE_FOLDER'] = WEBFILE_FOLDER
app.config["CACHE_TYPE"] = "null"
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024    # 1 Mb limit
app.config['1.img'] = app.config['UPLOAD_FOLDER'] + "/1.img"
app.config['2.img'] = app.config['UPLOAD_FOLDER'] + "/2.img"
app.image_fn = os.path.join(app.config['UPLOAD_FOLDER'], "image.jpg")
app.result_fn = os.path.join(app.config['UPLOAD_FOLDER'], "result.txt")
app.filename = ""
        
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

from handy.misc import switch

def getfeatures(filepath):
    colr = cv2.imread(filepath, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(colr, cv2.COLOR_BGR2GRAY)
    faces = app.detector.detect(gray)
    landmarks = app.aligner.align(gray, faces[0])
    features = app.identifier.extract_feature_with_crop(colr, landmarks)
    return features

def calcsim():
    feat1 = getfeatures(app.config['1.img'])
    feat2 = getfeatures(app.config['2.img'])
    return app.identifier.calc_similarity(feat1,feat2)

import json

@app.route('/face_match', methods=['POST'])
def face_match():
    if request.method == 'POST':
        # check if the post request has the file part
        if ('file1' in request.files) and ('file2' in request.files):        
            f1 = request.files.get('file1')
            f2 = request.files.get('file2')
            f1.save(app.config['1.img'],buffer_size=app.config['MAX_CONTENT_LENGTH'])
            f2.save(app.config['2.img'],buffer_size=app.config['MAX_CONTENT_LENGTH'])
            ret = calcsim()
            resp_data = {"sim": str(ret)} # convert numpy._bool to bool for json.dumps
            return json.dumps(resp_data)      

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')