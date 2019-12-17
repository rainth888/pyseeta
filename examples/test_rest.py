import requests
import json

db = "data/"

def test_face_match():
    url = 'http://0.0.0.0:5000/face_match'
    # open file in binary mode
    files = {'file1': open(db+'1.jpg', 'rb'),
             'file2': open(db+'2.jpeg', 'rb')}     
    resp = requests.post(url, files=files)
    print(json.dumps(resp.json()) )
    
if __name__ == '__main__':
    test_face_match()