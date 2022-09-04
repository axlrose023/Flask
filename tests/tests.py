from enum import Enum

import requests
from flask import url_for


class StaticMessages(Enum):
    WRONG_STATUS_CODE = 'Wrong status code'


def test_home():
    response = requests.get('http://127.0.0.1:5000/')
    assert response.status_code == 200, StaticMessages.WRONG_STATUS_CODE.value


def test_about():
    response = requests.get('http://127.0.0.1:5000/about')
    assert response.status_code == 200, StaticMessages.WRONG_STATUS_CODE.value


def test_login():
    response = requests.get('http://127.0.0.1:5000/login')
    assert response.status_code == 200, StaticMessages.WRONG_STATUS_CODE.value


def test_register():
    response = requests.get('http://127.0.0.1:5000/register')
    assert response.status_code == 200, StaticMessages.WRONG_STATUS_CODE.value

def test_profile():
    response = requests.get('http://127.0.0.1:5000/profile')
    assert response.status_code == 500, 'Allowed'


