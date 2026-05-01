from ..repositories.note_repository import NoteRepository
from ..exceptions import ValidationError, NotFoundError


COMPLETED_MAP = {'true': True, 'false': False}


class NoteService:

    def __init__(self, repo):
        self.repo = repo

    def list_notes(self, completed=None):
        if completed and completed.lower() not in COMPLETED_MAP:
            raise ValidationError("completed must be 'true' or 'false'")
        filter_val = COMPLETED_MAP.get(completed.lower()) if completed else None
        return [n.to_dict() for n in self.repo.get_all(completed=filter_val)]

    def get_note(self, note_id):
        note = self.repo.get_by_id(note_id)
        if note is None:
            raise NotFoundError(f'Note with id {note_id} not found')
        return note.to_dict()

    def create_note(self, data):
        self._validate_title(data.get('title'))
        completed = data.get('completed', False)
        if type(completed) != bool:
            raise ValidationError('completed must be a boolean')
        note = self.repo.create(
            title=data['title'].strip(),
            content=data.get('content'),
            completed=completed
        )
        return note.to_dict()

    def update_note(self, note_id, data):
        if self.repo.get_by_id(note_id) is None:
            raise NotFoundError(f'Note with id {note_id} not found')

        updates = {}
        if 'title' in data:
            self._validate_title(data['title'])
            updates['title'] = data['title'].strip()
        if 'content' in data:
            updates['content'] = data['content']
        if 'completed' in data:
            if type(data['completed']) != bool:
                raise ValidationError('completed must be a boolean')
            updates['completed'] = data['completed']

        return self.repo.update(note_id, **updates).to_dict()

    def delete_note(self, note_id):
        if not self.repo.delete(note_id):
            raise NotFoundError(f'Note with id {note_id} not found')

    def _validate_title(self, title):
        if title is None:
            raise ValidationError('title is required')
        if not str(title).strip():
            raise ValidationError('title cannot be empty')
        if len(str(title).strip()) > 100:
            raise ValidationError('title cannot exceed 100 characters')
