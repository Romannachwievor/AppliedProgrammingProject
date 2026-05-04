import pytest
import requests
from faker import Faker

name_faker = Faker()

BASE_URL = "http://localhost:8000"


def test_read_root():
    """Test the root endpoint returns Hello World message"""
    response = requests.get(f"{BASE_URL}/")

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Hello World!"


def test_check_404_error():
    response = requests.get(f"{BASE_URL}/nonexistent")
    assert response.status_code == 404


def test_check_greetings():
    name = "Martin"
    response = requests.get(f"{BASE_URL}/greetings/{name}")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Hello {name}!"


def test_greetings():
    for _ in range(10):
        name = name_faker.first_name()
        response = requests.get(f"{BASE_URL}/greetings/{name}")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Hello {name}!"


def test_is_adult():
    """Test if Check Adult works"""
    for age in range(0, 40):
        adult = age >= 18
        response = requests.get(f"{BASE_URL}/is-adult/{age}")
        assert response.status_code == 200
        data = response.json()
        for key in ["is_adult", "can_drive", "can_vote"]:
            assert data[key] == adult
        assert data["age"] == age
