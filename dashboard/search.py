import requests
import json
import hashlib
import random
from base64 import b64encode
from datetime import datetime
from wsse.client.requests.auth import WSSEAuth

def get_student_picture(student_id):
    student_info = get_student_info(student_id)
    return student_info['photo_link']

def get_student_major(student_id):
    student_info = get_student_info(student_id)
    return student_info['major_code']

def get_student_class(student_id):
    student_info = get_student_info(student_id)
    return student_info['class_year']

def get_student_info(student_id):
    # Following 2 lines are necessary to avoid IncompleteRead errors associated with urllib2
    # urllib2 was used instead of requests because using requests library was resulting in HTTPSConnectionPool errors
    httplib.HTTPConnection._http_vsn = 10
    httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

    url = 'https://tigerbook.herokuapp.com/api/v1/undergraduates/' + str(student_id)
    created = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    nonce = ''.join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/=') for i in range(32)])

    username = 'llbrower'
    password = '308435268dd61beca5152b328721ab6c'
    generated_digest = b64encode(hashlib.sha256(nonce + created + password).digest())
    headers = {
        'Authorization': 'WSSE profile="UsernameToken"',
        'X-WSSE': 'UsernameToken Username="%s", PasswordDigest="%s", Nonce="%s", Created="%s"' % (username, generated_digest, nonce, created)
    }

    request = urllib2.Request(url)
    request.add_header('Authorization', headers['Authorization'])
    request.add_header('X-WSSE', headers['X-WSSE'])
    response = urllib2.urlopen(request)
    return response.read()