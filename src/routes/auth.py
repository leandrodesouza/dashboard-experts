from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from src.models.auth import Coordenador
from src.models.user import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username e password são obrigatórios'}), 400
    
    coordenador = Coordenador.query.filter_by(username=username).first()
    
    if coordenador and coordenador.check_password(password) and coordenador.ativo:
        login_user(coordenador, remember=True)
        return jsonify({
            'success': True,
            'message': 'Login realizado com sucesso',
            'user': coordenador.to_dict()
        })
    else:
        return jsonify({'error': 'Credenciais inválidas'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True, 'message': 'Logout realizado com sucesso'})

@auth_bp.route('/status', methods=['GET'])
def status():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': current_user.to_dict()
        })
    else:
        return jsonify({'authenticated': False})

@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    data = request.json
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        return jsonify({'error': 'Senha atual e nova senha são obrigatórias'}), 400
    
    if not current_user.check_password(current_password):
        return jsonify({'error': 'Senha atual incorreta'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': 'Nova senha deve ter pelo menos 6 caracteres'}), 400
    
    current_user.set_password(new_password)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Senha alterada com sucesso'})

