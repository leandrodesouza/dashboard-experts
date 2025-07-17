from flask import Blueprint, jsonify, request
from src.models.demanda import Demanda, db
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/demandas', methods=['GET'])
def get_demandas():
    demandas = Demanda.query.all()
    return jsonify([demanda.to_dict() for demanda in demandas])

@dashboard_bp.route('/demandas', methods=['POST'])
def create_demanda():
    data = request.json
    demanda = Demanda(
        professor=data['professor'],
        disciplina=data.get('disciplina', ''),
        tipo_conteudo=data['tipo_conteudo'],
        data_envio=datetime.now().date(),
        prazo_entrega=datetime.strptime(data['prazo_entrega'], '%Y-%m-%d').date()
    )
    db.session.add(demanda)
    db.session.commit()
    return jsonify(demanda.to_dict()), 201

@dashboard_bp.route('/demandas/<int:demanda_id>', methods=['PUT'])
def update_demanda(demanda_id):
    demanda = Demanda.query.get_or_404(demanda_id)
    data = request.json
    
    # Atualizar campos de resultado
    if 'material_entregue' in data:
        demanda.material_entregue = data['material_entregue']
    if 'data_entrega' in data:
        demanda.data_entrega = datetime.strptime(data['data_entrega'], '%Y-%m-%d').date()
    if 'conformidade_roteiro' in data:
        demanda.conformidade_roteiro = data['conformidade_roteiro']
    if 'plataforma_publicacao' in data:
        demanda.plataforma_publicacao = data['plataforma_publicacao']
    if 'alcance_professor' in data:
        demanda.alcance_professor = data['alcance_professor']
    if 'impressoes_professor' in data:
        demanda.impressoes_professor = data['impressoes_professor']
    if 'curtidas_professor' in data:
        demanda.curtidas_professor = data['curtidas_professor']
    if 'comentarios_professor' in data:
        demanda.comentarios_professor = data['comentarios_professor']
    if 'compartilhamentos_professor' in data:
        demanda.compartilhamentos_professor = data['compartilhamentos_professor']
    if 'salvos_professor' in data:
        demanda.salvos_professor = data['salvos_professor']
    if 'visualizacoes_professor' in data:
        demanda.visualizacoes_professor = data['visualizacoes_professor']
    
    db.session.commit()
    return jsonify(demanda.to_dict())

@dashboard_bp.route('/demandas/<int:demanda_id>', methods=['DELETE'])
def delete_demanda(demanda_id):
    demanda = Demanda.query.get_or_404(demanda_id)
    db.session.delete(demanda)
    db.session.commit()
    return '', 204

@dashboard_bp.route('/estatisticas', methods=['GET'])
def get_estatisticas():
    demandas = Demanda.query.all()
    
    total_demandas = len(demandas)
    materiais_entregues = len([d for d in demandas if d.material_entregue == 'Sim'])
    alcance_total = sum([d.alcance_professor or 0 for d in demandas])
    curtidas_total = sum([d.curtidas_professor or 0 for d in demandas])
    comentarios_total = sum([d.comentarios_professor or 0 for d in demandas])
    
    engajamento_medio = 0
    if alcance_total > 0:
        engajamento_medio = ((curtidas_total + comentarios_total) / alcance_total) * 100
    
    return jsonify({
        'total_demandas': total_demandas,
        'materiais_entregues': materiais_entregues,
        'alcance_total': alcance_total,
        'engajamento_medio': round(engajamento_medio, 1)
    })

@dashboard_bp.route('/professores/estatisticas', methods=['GET'])
def get_estatisticas_professores():
    demandas = Demanda.query.all()
    professores_stats = {}
    
    professores = [
        'Pedro Campos', 'Pablo', 'Rafael Araújo', 'Samuel', 'Tiago Vidal',
        'Rogério Dalvipa', 'Lucas Fávero', 'Pedro Canezin', 'Filipe Ávila',
        'João Paulo', 'Heitor'
    ]
    
    for professor in professores:
        demandas_prof = [d for d in demandas if d.professor == professor]
        entregues_prof = [d for d in demandas_prof if d.material_entregue == 'Sim']
        
        professores_stats[professor] = {
            'demandas': len(demandas_prof),
            'entregues': len(entregues_prof),
            'alcance_total': sum([d.alcance_professor or 0 for d in demandas_prof]),
            'curtidas_total': sum([d.curtidas_professor or 0 for d in demandas_prof])
        }
    
    return jsonify(professores_stats)

