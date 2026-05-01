from flask import Blueprint, request, jsonify
from ..services.note_service import NoteService
from ..repositories.note_repository import NoteRepository
from ..exceptions import ValidationError, NotFoundError

notes_bp = Blueprint('notes', __name__)


def _get_service():
    return NoteService(NoteRepository())


@notes_bp.route('', methods=['GET'])
def get_notes():
    completed = request.args.get('completed')
    svc = _get_service()
    try:
        return jsonify(svc.list_notes(completed=completed)), 200
    except ValidationError as e:
        return jsonify({'error': e.message}), 400


@notes_bp.route('/<int:note_id>', methods=['GET'])
def get_note(note_id):
    svc = _get_service()
    try:
        return jsonify(svc.get_note(note_id)), 200
    except NotFoundError as e:
        return jsonify({'error': e.message}), 404


@notes_bp.route('', methods=['POST'])
def create_note():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'error': 'invalid JSON'}), 400
    svc = _get_service()
    try:
        return jsonify(svc.create_note(body)), 201
    except ValidationError as e:
        return jsonify({'error': e.message}), 400


@notes_bp.route('/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'error': 'invalid JSON'}), 400
    svc = _get_service()
    try:
        return jsonify(svc.update_note(note_id, body)), 200
    except NotFoundError as e:
        return jsonify({'error': e.message}), 404
    except ValidationError as e:
        return jsonify({'error': e.message}), 400


@notes_bp.route('/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    svc = _get_service()
    try:
        svc.delete_note(note_id)
        return '', 204
    except NotFoundError as e:
        return jsonify({'error': e.message}), 404
