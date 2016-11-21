import requests
from wsse.client.requests.auth import WSSEAuth

def get_quiz_data():
    wsse_auth = WSSEAuth('llbrower', 'FYDvNGIRqfrUyXBKfmlmsBXDhLVBAZRzJFqhWmTFihnnBPVMGoykJTydJCoVvSPh')
    resp = requests.get('http://localhost:8000/api/v1/quizzes/', auth = wsse_auth)
    return resp.json()

def get_attempt_data():
    wsse_auth = WSSEAuth('llbrower', 'FYDvNGIRqfrUyXBKfmlmsBXDhLVBAZRzJFqhWmTFihnnBPVMGoykJTydJCoVvSPh')
    resp = requests.get('http://localhost:8000/api/v1/attempts/', auth = wsse_auth)
    return resp.json()

def get_user_data():
    wsse_auth = WSSEAuth('llbrower', 'FYDvNGIRqfrUyXBKfmlmsBXDhLVBAZRzJFqhWmTFihnnBPVMGoykJTydJCoVvSPh')
    resp = requests.get('http://localhost:8000/api/v1/users/', auth = wsse_auth)
    return resp.json()

def get_student_name(student_id):
    users_json = get_user_data()

    for user in users_json:
        id = user['email'].split('@')[0]
        if (id == student_id):
            return user['first_name'] + ' ' + user['last_name']

    return ""