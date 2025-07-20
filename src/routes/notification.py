from flask import Blueprint, request, jsonify
from flask_login import login_required
from src.models.template import TemplateNotificacao, NotificacaoEnviada
from src.models.demanda import Demanda
from src.services.notification import NotificationService
from src.models.user import db

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/templates', methods=['GET'])
@login_required
def get_templates():
    """Lista todos os templates de notificação"""
    templates = TemplateNotificacao.query.filter_by(ativo=True).all()
    return jsonify([template.to_dict() for template in templates])

@notification_bp.route('/templates', methods=['POST'])
@login_required
def create_template():
    """Cria um novo template de notificação"""
    data = request.json
    
    template = TemplateNotificacao(
        nome=data['nome'],
        tipo=data['tipo'],
        assunto=data.get('assunto'),
        conteudo=data['conteudo']
    )
    
    db.session.add(template)
    db.session.commit()
    
    return jsonify(template.to_dict()), 201

@notification_bp.route('/templates/<int:template_id>', methods=['PUT'])
@login_required
def update_template(template_id):
    """Atualiza um template existente"""
    template = TemplateNotificacao.query.get_or_404(template_id)
    data = request.json
    
    template.nome = data.get('nome', template.nome)
    template.tipo = data.get('tipo', template.tipo)
    template.assunto = data.get('assunto', template.assunto)
    template.conteudo = data.get('conteudo', template.conteudo)
    template.ativo = data.get('ativo', template.ativo)
    
    db.session.commit()
    
    return jsonify(template.to_dict())

@notification_bp.route('/enviar', methods=['POST'])
@login_required
def enviar_notificacao():
    """Envia notificação para um professor"""
    data = request.json
    
    demanda_id = data.get('demanda_id')
    template_id = data.get('template_id')
    roteiro = data.get('roteiro', '')
    
    if not demanda_id or not template_id:
        return jsonify({'error': 'demanda_id e template_id são obrigatórios'}), 400
    
    # Buscar demanda
    demanda = Demanda.query.get(demanda_id)
    if not demanda:
        return jsonify({'error': 'Demanda não encontrada'}), 404
    
    # Preparar dados extras
    dados_extras = {
        'roteiro': roteiro
    }
    
    # Enviar notificação
    service = NotificationService()
    resultado = service.enviar_notificacao(demanda, template_id, dados_extras)
    
    if resultado['success']:
        return jsonify({
            'success': True,
            'message': resultado['message']
        })
    else:
        return jsonify({
            'success': False,
            'error': resultado['error']
        }), 400

@notification_bp.route('/historico', methods=['GET'])
@login_required
def get_historico_notificacoes():
    """Lista o histórico de notificações enviadas"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    notificacoes = NotificacaoEnviada.query.order_by(
        NotificacaoEnviada.enviado_em.desc()
    ).paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return jsonify({
        'notificacoes': [n.to_dict() for n in notificacoes.items],
        'total': notificacoes.total,
        'pages': notificacoes.pages,
        'current_page': page
    })

@notification_bp.route('/demanda/<int:demanda_id>/notificacoes', methods=['GET'])
@login_required
def get_notificacoes_demanda(demanda_id):
    """Lista notificações de uma demanda específica"""
    notificacoes = NotificacaoEnviada.query.filter_by(demanda_id=demanda_id).all()
    return jsonify([n.to_dict() for n in notificacoes])

@notification_bp.route('/configuracoes', methods=['GET'])
@login_required
def get_configuracoes():
    """Retorna as configurações de notificação"""
    import os
    
    return jsonify({
        'email_configurado': bool(os.getenv('EMAIL_USER') and os.getenv('EMAIL_PASSWORD')),
        'whatsapp_configurado': bool(os.getenv('WHATSAPP_API_URL') and os.getenv('WHATSAPP_TOKEN')),
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587'))
    })

@notification_bp.route('/teste', methods=['POST'])
@login_required
def teste_notificacao():
    """Testa o envio de notificação"""
    data = request.json
    tipo = data.get('tipo')  # 'email' ou 'whatsapp'
    destinatario = data.get('destinatario')
    
    if not tipo or not destinatario:
        return jsonify({'error': 'Tipo e destinatário são obrigatórios'}), 400
    
    service = NotificationService()
    
    if tipo == 'email':
        resultado = service.enviar_email(
            destinatario, 
            'Teste - Dashboard Projeto Experts',
            'Esta é uma mensagem de teste do sistema de notificações.'
        )
    elif tipo == 'whatsapp':
        resultado = service.enviar_whatsapp(
            destinatario,
            '🧪 *Teste* - Dashboard Projeto Experts\n\nEsta é uma mensagem de teste do sistema de notificações.'
        )
    else:
        return jsonify({'error': 'Tipo não suportado'}), 400
    
    return jsonify(resultado)

