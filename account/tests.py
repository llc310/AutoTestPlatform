# Create your tests here.


def test_post_login(user_client):
    response = user_client.post(
        path="/api/account/profile/login/",
        data={"username": "test_user", "password": "test_user_pass"},
        content_type="application/json",
    )

    assert 200 == response.status_code
    assert 1 == response.data["id"]


def test_post_reset_password(user_api_client):
    response = user_api_client.post(
        path="/api/account/profile/reset_password/",
        data={"new_password": "123456", "confirm_password": "123456"},
        content_type="application/json",
    )
    assert 204 == response.status_code

    user_api_client.logout()

    response = user_api_client.post(
        path="/api/account/profile/login/",
        data={"username": "test_user", "password": "123456"},
        content_type="application/json",
    )
    assert 200 == response.status_code
    assert 1 == response.data["id"]


def test_get_profile(user_api_client):
    response = user_api_client.get(path="/api/account/profile/profile/")
    assert 200 == response.status_code
    assert 1 == response.data["id"]


def test_post_change(user_api_client):
    try:
        file = open(file=r"D:\SnipastePicture\llc3.png", mode="rb")
        response = user_api_client.post(
            path="/api/account/profile/change/",
            data={"name": "test001", "head_img": file},
        )
        assert 200 == response.status_code
        assert "test001" in response.data["name"]
        assert ".png" in response.data["head_img"]
        assert "llc3" in response.data["head_img"]
    finally:
        file.close()
