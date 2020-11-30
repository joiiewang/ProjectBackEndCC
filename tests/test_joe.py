import json
from base64 import b64encode

# Database is reset between tests
# Not sure if this is the best way to do things

def test_joe(app,client):
    res = client.post('/api/v2/users/',json={"username":"joe","password":"monkey"})
    assert res.status_code == 200 # success

    res = client.get('/api/v2/users/')
    assert res.status_code == 200 # success
    assert (json.loads(res.get_data(as_text=True)) ==
    [{'id':1,'points':0,'trees':0,'username':'joe'}])

    #Test invalid credentials
    credentials = b64encode(b"joe:monke").decode('utf-8')
    auth_headers = {"Authorization":f"Basic {credentials}"}
    res = client.get('/api/v2/users/joe/',headers=auth_headers)
    assert res.status_code == 401

    #Use correct credentials from now on
    credentials = b64encode(b"joe:monkey").decode('utf-8')
    auth_headers = {"Authorization":f"Basic {credentials}"}

    #Get self
    res = client.get('/api/v2/users/joe/',headers=auth_headers)
    assert res.status_code == 200
    assert (json.loads(res.get_data(as_text=True)) ==
    {'id':1,'points':0,'trees':0,'username':'joe'})

    #List courses
    res = client.get('/api/v2/users/joe/courses/',headers=auth_headers)
    assert res.status_code == 200
    assert (json.loads(res.get_data(as_text=True)) ==
            [])

    #Create course 
    res = client.post('/api/v2/users/joe/courses/',headers=auth_headers,json={'name':'math'})
    assert res.status_code == 200
    assert (json.loads(res.get_data(as_text=True)) ==
            {'id':1,'name':'math',"links":[],"notes":[],"todos":[]})

    #List courses
    res = client.get('/api/v2/users/joe/courses/',headers=auth_headers)
    assert res.status_code == 200
    assert (json.loads(res.get_data(as_text=True)) ==
            [{'id':1,'name':'math',"links":[],"notes":[],"todos":[]}])

    #Delete course 
    res = client.delete('/api/v2/users/joe/courses/1/',headers=auth_headers)
    assert res.status_code == 200

    #List courses
    res = client.get('/api/v2/users/joe/courses/',headers=auth_headers)
    assert res.status_code == 200
    assert (json.loads(res.get_data(as_text=True)) ==
            [])
