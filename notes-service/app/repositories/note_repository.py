from datetime import datetime
from ..models.note import Note
from .. import db


class NoteRepository:

    def get_all(self, completed=None):
        query = Note.query
        if completed is not None:
            query = query.filter_by(completed=completed)
        return query.all()

    def get_by_id(self, id):
        return db.session.get(Note, id)

    def create(self, title, content, completed):
        note = Note(title=title, content=content, completed=completed)
        db.session.add(note)
        db.session.commit()
        return note

    def update(self, id, **data):
        note = db.session.get(Note, id)
        if not note:
            return None
        if 'title' in data:
            note.title = data['title']
        if 'content' in data:
            note.content = data['content']
        if 'completed' in data:
            note.completed = data['completed']
        note.updated_at = datetime.utcnow()
        db.session.commit()
        return note

    def delete(self, id):
        note = db.session.get(Note, id)
        if not note:
            return False
        db.session.delete(note)
        db.session.commit()
        return True
