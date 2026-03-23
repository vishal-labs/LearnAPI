def test_signup(client, random_email):
    response = client.post(
        "/auth/signup",
        json={"username": "testuser", "email": random_email, "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["msg"] == "Account created"

def test_login(client, random_email):
    response = client.post(
        "/auth/login",
        json={"email": random_email, "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "refresh_token" in data

def test_refresh_token(client, random_email):
    login_resp = client.post(
        "/auth/login",
        json={"email": random_email, "password": "password123"}
    )
    refresh_token = login_resp.json()["refresh_token"]
    
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_forgot_password(client, random_email):
    response = client.post(
        "/auth/forgot-password",
        json={"email": random_email}
    )
    assert response.status_code == 200
    assert "reset link was sent" in response.json()["msg"]
