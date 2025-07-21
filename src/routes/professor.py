from flask import Blueprint, request, jsonify
from src.models.professor import Professor
from src.db import db

professor_bp = Blueprint('professor', __name__)

# Rota para adicionar professor
@professor_bp.route('/', methods=['POST'])
def adicionar_professor():
    data = request.json

    novo_professor = Professor(
        nome=data.get('nome'),
        disciplinas=data.get('disciplinas'),
        instagram=data.get('instagram'),
        email=data.get('email'),
        whatsapp=data.get('whatsapp')
    )

    db.session.add(novo_professor)
    db.session.commit()

    return jsonify({'message': 'Professor cadastrado com sucesso!', 'id': novo_professor.id}), 201

# Rota para listar todos os professores
@professor_bp.route('/', methods=['GET'])
def listar_professores():
    professores = Professor.query.all()
    return jsonify([p.to_dict() for p in professores])
