from src.db import db
from datetime import datetime

class TemplateNotificacao(db.Model):
    __tablename__ = 'templates_notificacao'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    assunto = db.Column(db.String(200))
    conteudo = db.Column(db.Text, nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo,
            'assunto': self.assunto,
            'conteudo': self.conteudo,
            'ativo': self.ativo,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None
        }

    @staticmethod
    def create_default_templates():
        if not TemplateNotificacao.query.first():
            template_email = TemplateNotificacao(
                nome='Roteiro Padrão - E-mail',
                tipo='email',
                assunto='Novo Roteiro - Projeto Experts AlfaCon',
                conteudo="""Olá {professor_nome},

Esperamos que esteja bem!

Temos um novo roteiro para você no Projeto Experts:

📋 **Detalhes da Demanda:**
- **Tipo de Conteúdo:** {tipo_conteudo}
- **Prazo de Entrega:** {prazo_entrega}
- **Data de Envio:** {data_envio}

📝 **Roteiro:**
{roteiro_personalizado}

📌 **Instruções Importantes:**
- Por favor, siga o roteiro fornecido para manter a consistência da marca
- Lembre-se de incluir as hashtags sugeridas
- Envie o material finalizado até a data limite
- Em caso de dúvidas, entre em contato conosco

Obrigado pela sua dedicação ao Projeto Experts!

Atenciosamente,
Equipe AlfaCon"""
            )

            template_whatsapp = TemplateNotificacao(
                nome='Roteiro Padrão - WhatsApp',
                tipo='whatsapp',
                conteudo="""🎯 *Novo Roteiro - Projeto Experts*

Olá {professor_nome}! 

📋 *Detalhes:*
• Tipo: {tipo_conteudo}
• Prazo: {prazo_entrega}

📝 *Roteiro:*
{roteiro_personalizado}

📌 *Lembre-se:*
✅ Seguir o roteiro
✅ Incluir hashtags
✅ Entregar no prazo

Dúvidas? É só chamar! 😊

*Equipe AlfaCon* 🚀"""
            )

            db.session.add(template_email)
            db.session.add(template_whatsapp)
            db.session.commit()
            return [template_email, template_whatsapp]
        return []

class NotificacaoEnviada(db.Model):
    __tablename__ = 'notificacoes_enviadas'

    id = db.Column(db.Integer, primary_key=True)
    demanda_id = db.Column(db.Integer, nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates_notificacao.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    destinatario = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='enviado')
    erro_detalhes = db.Column(db.Text)
    enviado_em = db.Column(db.DateTime, default=datetime.utcnow)

    template = db.relationship('TemplateNotificacao', backref='envios')

    def to_dict(self):
        return {
            'id': self.id,
            'demanda_id': self.demanda_id,
            'template_id': self.template_id,
            'tipo': self.tipo,
            'destinatario': self.destinatario,
            'status': self.status,
            'erro_detalhes': self.erro_detalhes,
            'enviado_em': self.enviado_em.isoformat() if self.enviado_em else None
        }
