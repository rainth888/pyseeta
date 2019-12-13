from pyseeta import Detector
from pyseeta import Aligner
from pyseeta import Identifier

try:
    import cv2
    import numpy as np
except ImportError:
    raise ImportError('opencv can not be found!')

ALI_MODEL_PATH = "models/seeta_fa_v1.1.bin"
DET_MODEL_PATH = "models/seeta_fd_frontal_v1.0.bin"
REC_MODEL_PATH = "models/seeta_fr_v1.0.bin"

import os

def release(ali,det,rec):
    ali.release()
    det.release()
    rec.release()

def resize(image,W=400.):
    _, width, _ = image.shape
    imgScale = W/width
    newX,newY = image.shape[1]*imgScale, image.shape[0]*imgScale
    return cv2.resize(image,(int(newX),int(newY)))

def test_recognition(img_path,db_path):
    if not os.path.isfile(img_path) or not os.path.isdir(db_path): 
        print("indicated path doesn't exist!");return

    # load model
    detector = Detector(DET_MODEL_PATH)
    aligner = Aligner(ALI_MODEL_PATH)
    identifier = Identifier(REC_MODEL_PATH)

    # load test image
    image_color_A = cv2.imread(img_path, cv2.IMREAD_COLOR)
    image_gray_A = cv2.cvtColor(image_color_A, cv2.COLOR_BGR2GRAY)
    faces_A = detector.detect(image_gray_A)

    # load database
    for fn in os.listdir(db_path):
        fp = os.path.join(db_path,fn)
        if not os.path.isfile(fp): continue
        image_color_B = cv2.imread(fp, cv2.IMREAD_COLOR)
        image_gray_B = cv2.cvtColor(image_color_B, cv2.COLOR_BGR2GRAY)
        # detect face in image
        faces_B = detector.detect(image_gray_B)
        if len(faces_A) and len(faces_B):
            landmarks_A = aligner.align(image_gray_A, faces_A[0])
            featA = identifier.extract_feature_with_crop(image_color_A, landmarks_A)
            # cv2.rectangle(image_color_A, (faces_A[0].left, faces_A[0].top), (faces_A[0].right, faces_A[0].bottom), (0,255,0), thickness=2)
            sim_list = []
            for face in faces_B:
                landmarks_B = aligner.align(image_gray_B, face)
                featB = identifier.extract_feature_with_crop(image_color_B, landmarks_B)
                sim = identifier.calc_similarity(featA, featB)
                sim_list.append(sim)
            print('sim: {}'.format(sim_list))
            # index = np.argmax(sim_list)
            for i, face in enumerate(faces_B):
                color = (0,255,0) if sim_list[i] > 0.5 else (0,0,255)
                cv2.rectangle(image_color_B, (face.left, face.top), (face.right, face.bottom), color, thickness=2)
            # cv2.imshow('test', resize(image_color_A))
            cv2.imshow('double', resize(image_color_B))
            cv2.waitKey(0)

    release(aligner,detector,identifier)

if __name__ == '__main__':
    # imgpath = raw_input("test image path: ")
    # dbpath = raw_input("database path:")
    path = "/media/ubuntu/Investigation/DataSet/Image/Face"
    imgpath = path + "/sample.jpg"
    dbpath = path + "/db"
    test_recognition(imgpath,dbpath)