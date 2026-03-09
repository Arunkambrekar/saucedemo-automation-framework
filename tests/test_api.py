import requests
import pytest

BASE = "https://jsonplaceholder.typicode.com"

def test_get_users_status_200():
    r = requests.get(f"{BASE}/users")
    assert r.status_code == 200

def test_get_users_returns_list():
    r = requests.get(f"{BASE}/users")
    data = r.json()
    assert len(data) > 0

def test_create_user():
    r = requests.post(f"{BASE}/posts",
        json={"title": "QA Test", "body": "Automation", "userId": 1})
    assert r.status_code == 201
    assert r.json()["title"] == "QA Test"

def test_update_user():
    r = requests.put(f"{BASE}/posts/1",
        json={"id": 1, "title": "Updated", "body": "QA", "userId": 1})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"

def test_delete_user():
    r = requests.delete(f"{BASE}/posts/1")
    assert r.status_code == 200

def test_user_not_found():
    r = requests.get(f"{BASE}/posts/99999")
    assert r.status_code == 404