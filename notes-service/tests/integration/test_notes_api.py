import pytest
from app import create_app, db


@pytest.fixture
def app():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_notes_empty(client):
    res = client.get('/notes')
    assert res.status_code == 200
    assert res.get_json() == []


def test_get_notes_returns_all(client):
    client.post('/notes', json={'title': 'Note 1'})
    client.post('/notes', json={'title': 'Note 2'})
    res = client.get('/notes')
    assert res.status_code == 200
    assert len(res.get_json()) == 2


def test_get_notes_filter_true(client):
    client.post('/notes', json={'title': 'Done', 'completed': True})
    client.post('/notes', json={'title': 'Pending'})
    res = client.get('/notes?completed=true')
    data = res.get_json()
    assert res.status_code == 200
    assert len(data) == 1
    assert data[0]['completed'] is True


def test_get_notes_filter_false(client):
    client.post('/notes', json={'title': 'Done', 'completed': True})
    client.post('/notes', json={'title': 'Pending'})
    res = client.get('/notes?completed=false')
    data = res.get_json()
    assert res.status_code == 200
    assert len(data) == 1
    assert data[0]['completed'] is False


def test_get_notes_bad_filter(client):
    res = client.get('/notes?completed=maybe')
    assert res.status_code == 400


def test_get_note_by_id(client):
    r = client.post('/notes', json={'title': 'My Note'})
    nid = r.get_json()['id']
    res = client.get(f'/notes/{nid}')
    assert res.status_code == 200
    assert res.get_json()['title'] == 'My Note'


def test_get_note_not_found(client):
    res = client.get('/notes/9999')
    assert res.status_code == 404
    assert 'error' in res.get_json()


def test_create_note_ok(client):
    res = client.post('/notes', json={'title': 'Buy groceries'})
    assert res.status_code == 201
    data = res.get_json()
    assert data['title'] == 'Buy groceries'
    assert data['completed'] is False
    assert 'id' in data
    assert 'created_at' in data


def test_create_note_with_content(client):
    res = client.post('/notes', json={'title': 'Task', 'content': 'Details here'})
    assert res.status_code == 201
    assert res.get_json()['content'] == 'Details here'


def test_create_no_title(client):
    res = client.post('/notes', json={'content': 'No title'})
    assert res.status_code == 400


def test_create_empty_title(client):
    res = client.post('/notes', json={'title': ''})
    assert res.status_code == 400


def test_create_whitespace_title(client):
    res = client.post('/notes', json={'title': '   '})
    assert res.status_code == 400


def test_create_title_too_long(client):
    res = client.post('/notes', json={'title': 'x' * 101})
    assert res.status_code == 400


def test_create_no_body(client):
    res = client.post('/notes', content_type='application/json', data='')
    assert res.status_code == 400


def test_create_wrong_content_type(client):
    res = client.post('/notes', data='title=test')
    assert res.status_code == 400


def test_update_note_ok(client):
    r = client.post('/notes', json={'title': 'Original'})
    nid = r.get_json()['id']
    res = client.put(f'/notes/{nid}', json={'title': 'Updated', 'completed': True})
    assert res.status_code == 200
    data = res.get_json()
    assert data['title'] == 'Updated'
    assert data['completed'] is True


def test_update_note_not_found(client):
    res = client.put('/notes/9999', json={'title': 'X'})
    assert res.status_code == 404


def test_update_note_empty_title(client):
    r = client.post('/notes', json={'title': 'Original'})
    nid = r.get_json()['id']
    res = client.put(f'/notes/{nid}', json={'title': ''})
    assert res.status_code == 400


def test_delete_note_ok(client):
    r = client.post('/notes', json={'title': 'Delete me'})
    nid = r.get_json()['id']
    res = client.delete(f'/notes/{nid}')
    assert res.status_code == 204
    assert res.data == b''


def test_delete_note_not_found(client):
    res = client.delete('/notes/9999')
    assert res.status_code == 404


def test_delete_actually_removes(client):
    r = client.post('/notes', json={'title': 'Temp'})
    nid = r.get_json()['id']
    client.delete(f'/notes/{nid}')
    assert client.get(f'/notes/{nid}').status_code == 404
