import pytest
from django.contrib.auth.models import User
from django.test import Client
from rest_framework.test import APIClient


@pytest.fixture()
def client():
    return Client()


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def user(_django_db_helper):
    return User.objects.create_user(
        username="test_user", email="test_user@qq.com", password="test_user_pass"
    )


@pytest.fixture()
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture()
def user_api_client(user, api_client):
    api_client.force_authenticate(user)
    return api_client
