import json

#Database should be reset between tests

def test_empty_list_users(app,client):
    res = client.get('/api/v2/users/')
    assert res.status_code == 200 # success
    assert [] == json.loads(res.get_data(as_text=True))

def test_get_unauth_user(app,client):
    res = client.get('/api/v2/users/joe/')
    assert res.status_code == 401 # unauthorized

def test_create_user_no_password(app,client):
    res = client.post('/api/v2/users/',json={"username":"joe"})
    assert res.status_code == 400 # bad request

def test_create_user(app,client):
    res = client.post('/api/v2/users/',json={"username":"joe","password":"monkey"})
    assert res.status_code == 200 # success

def test_create_user_twice(app,client):
    res = client.post('/api/v2/users/',json={"username":"joe","password":"monkey"})
    assert res.status_code == 200 # success
    res = client.post('/api/v2/users/',json={"username":"joe","password":"monkey"})
    assert res.status_code == 422 # unprocessable entity

