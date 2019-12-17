import requests
import json

db = "/media/ubuntu/Investigation/DataSet/Image/Face/db/"

def test_face_match():
    url = 'http://127.0.0.1:5000/face_match'
    # open file in binary mode
    files = {'file1': open(db+'3.jpg', 'rb'),
             'file2': open(db+'4.jpg', 'rb')}     
    resp = requests.post(url, files=files)
    print( 'face_match response:\n', json.dumps(resp.json()) )
    
if __name__ == '__main__':
    test_face_match()