from flask import Blueprint, jsonify, current_app
from ..clients.jsonplaceholder import JsonPlaceholderClient
from ..services.external_service import ExternalService, ExternalServiceError

external_bp = Blueprint('external', __name__)


def get_service():
    client = JsonPlaceholderClient(
        base_url=current_app.config['JSONPLACEHOLDER_BASE_URL'],
        timeout=current_app.config['EXTERNAL_API_TIMEOUT']
    )
    return ExternalService(client)


@external_bp.route('/users', methods=['GET'])
def get_users():
    svc = get_service()
    try:
        return jsonify(svc.get_users()), 200
    except ExternalServiceError as e:
        return jsonify({'error': str(e)}), 503


@external_bp.route('/posts', methods=['GET'])
def get_posts():
    svc = get_service()
    try:
        return jsonify(svc.get_posts()), 200
    except ExternalServiceError as e:
        return jsonify({'error': str(e)}), 503


@external_bp.route('/posts/<int:user_id>', methods=['GET'])
def get_posts_by_user(user_id):
    svc = get_service()
    try:
        return jsonify(svc.get_posts_by_user(user_id)), 200
    except ExternalServiceError as e:
        return jsonify({'error': str(e)}), 503
