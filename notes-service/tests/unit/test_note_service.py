import pytest
from unittest.mock import MagicMock
from app.services.note_service import NoteService
from app.exceptions import ValidationError, NotFoundError
from datetime import datetime


def fake_note(id=1, title='Test', content=None, completed=False):
    note = MagicMock()
    note.to_dict.return_value = {
        'id': id,
        'title': title,
        'content': content,
        'completed': completed,
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'updated_at': datetime.utcnow().isoformat() + 'Z',
    }
    return note


@pytest.fixture
def repo():
    return MagicMock()


@pytest.fixture
def svc(repo):
    return NoteService(repo)


def test_create_note_ok(svc, repo):
    repo.create.return_value = fake_note(title='Buy milk')
    result = svc.create_note({'title': 'Buy milk'})
    assert result['title'] == 'Buy milk'
    repo.create.assert_called_once_with(title='Buy milk', content=None, completed=False)


def test_create_strips_whitespace(svc, repo):
    repo.create.return_value = fake_note(title='Buy milk')
    svc.create_note({'title': '  Buy milk  '})
    repo.create.assert_called_once_with(title='Buy milk', content=None, completed=False)


def test_create_no_title_fails(svc, repo):
    with pytest.raises(ValidationError) as e:
        svc.create_note({'content': 'something'})
    assert 'required' in e.value.message


def test_create_empty_title_fails(svc, repo):
    with pytest.raises(ValidationError) as e:
        svc.create_note({'title': ''})
    assert 'empty' in e.value.message


def test_create_whitespace_only_title_fails(svc, repo):
    with pytest.raises(ValidationError) as e:
        svc.create_note({'title': '   '})
    assert 'empty' in e.value.message


def test_create_title_too_long_fails(svc, repo):
    with pytest.raises(ValidationError) as e:
        svc.create_note({'title': 'a' * 101})
    assert '100' in e.value.message


def test_create_with_completed_true(svc, repo):
    repo.create.return_value = fake_note(completed=True)
    svc.create_note({'title': 'Task', 'completed': True})
    repo.create.assert_called_once_with(title='Task', content=None, completed=True)


def test_create_completed_not_bool_fails(svc, repo):
    with pytest.raises(ValidationError):
        svc.create_note({'title': 'Task', 'completed': 'yes'})


def test_get_note_ok(svc, repo):
    repo.get_by_id.return_value = fake_note(id=1)
    result = svc.get_note(1)
    assert result['id'] == 1


def test_get_note_missing_raises_404(svc, repo):
    repo.get_by_id.return_value = None
    with pytest.raises(NotFoundError) as e:
        svc.get_note(99)
    assert '99' in e.value.message


def test_list_notes_no_filter(svc, repo):
    repo.get_all.return_value = [fake_note(id=1), fake_note(id=2)]
    result = svc.list_notes()
    assert len(result) == 2
    repo.get_all.assert_called_once_with(completed=None)


def test_list_notes_filter_true(svc, repo):
    repo.get_all.return_value = []
    svc.list_notes(completed='true')
    repo.get_all.assert_called_once_with(completed=True)


def test_list_notes_filter_false(svc, repo):
    repo.get_all.return_value = []
    svc.list_notes(completed='false')
    repo.get_all.assert_called_once_with(completed=False)


def test_list_notes_bad_filter_fails(svc, repo):
    with pytest.raises(ValidationError):
        svc.list_notes(completed='maybe')


def test_update_note_ok(svc, repo):
    repo.get_by_id.return_value = fake_note()
    repo.update.return_value = fake_note(title='Updated')
    result = svc.update_note(1, {'title': 'Updated'})
    assert result['title'] == 'Updated'


def test_update_note_not_found(svc, repo):
    repo.get_by_id.return_value = None
    with pytest.raises(NotFoundError):
        svc.update_note(99, {'title': 'X'})


def test_update_note_empty_title_fails(svc, repo):
    repo.get_by_id.return_value = fake_note()
    with pytest.raises(ValidationError):
        svc.update_note(1, {'title': ''})


def test_delete_note_ok(svc, repo):
    repo.delete.return_value = True
    svc.delete_note(1)
    repo.delete.assert_called_once_with(1)


def test_delete_note_not_found(svc, repo):
    repo.delete.return_value = False
    with pytest.raises(NotFoundError):
        svc.delete_note(99)
