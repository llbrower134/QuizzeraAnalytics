import requests
import json
import hashlib
import random
from base64 import b64encode
from datetime import datetime
from wsse.client.requests.auth import WSSEAuth

def get_student_picture(student_id):
    student_info = getStudentInfo(student_id)
    return student_info['photo_link']

def get_student_major(student_id):
    student_info = getStudentInfo(student_id)
    return student_info['major_code']

def get_student_class(student_id):
    student_info = getStudentInfo(student_id)
    return student_info['class_year']

def get_student_info(student_id):
    url = 'https://tigerbook.org/api/v1/undergraduates/llbrower'
    created = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    nonce = ''.join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/=') for i in range(32)])
    username = 'llbrower'
    password = 'b7f490fe8ad678a8cbc54826cd0c40e7'
    generated_digest = b64encode(hashlib.sha256((nonce + created + password).encode('utf-8')).digest())
    headers = {
        'Authorization': 'WSSE profile="UsernameToken"',
        'X-WSSE': 'UsernameToken Username="%s", PasswordDigest="%s", Nonce="%s", Created="%s"' % (username, generated_digest, nonce, created)
    }
    response = requests.get(url, headers=headers)
    return response