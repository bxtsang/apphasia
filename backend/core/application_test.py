import pytest
import requests
import json
import time

host = "http://localhost:5300"
def test_retrieve_core():
    url = f"{host}/core/1"
    response = requests.get(url)
    name = json.loads(response.text)['user']['name']

    assert name == "Cliffen Lee Jun Yi"

def test_retrieve_all_core():
    url = f"{host}/core"

    response = requests.get(url)
    users = json.loads(response.text)['users']

    assert len(users) >= 3

def test_add_core():
    url = f"{host}/core"

    getResponseBefore = requests.get(url)
    countBefore = len(json.loads(getResponseBefore.text)['users'])

    user = {"name": "billy tan", "email": "billytan@gmail.com", "phone": 98786787, "password": "billypass"}

    response = requests.post(url, json=user)

    getResponseAfter = requests.get(url)
    countAfter = len(json.loads(getResponseAfter.text)['users'])


    assert countAfter - countBefore == 1
