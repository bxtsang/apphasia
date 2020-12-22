import pytest
import requests
import json

def test_retrieve_core():
    url = "http://localhost:5300/core"
    data = {"email": "cliffen123@gmail.com",
            "password": "testtest"}
    response = requests.post(url, json=json.dumps(data))

    name = json.loads(response.text)['name']

    assert name == "Cliffen Lee Jun Yi"

def test_retrieve_all_core():
    url = "http://localhost:5300/core"

    response = requests.get(url).text

    assert response == json.dumps([{"name": "Cliffen Lee Jun Yi", "email": "cliffen123@gmail.com", "phone": 69798999, "password": "testtest"},
                                  {"name": "Glen See Saw", "email": "glenwaves@gmail.com", "phone": 99887766, "password": "test32"},
                                  {"name": "Mary Had Little Lamb", "email": "marydonut@gmail.com", "phone": 98897667, "password": "test324"}])
    