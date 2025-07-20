import smtplib
import requests
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from src.models.template import TemplateNotificacao, NotificacaoEnviada
from src.models.user import db

class NotificationService:
    def __init__(self):
        # Configurações de e-mail (podem ser definidas via variáveis de ambiente)
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_user = os.getenv('EMAIL_USER', '')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        
        # Configurações do WhatsApp (API externa - exemplo com Twilio ou similar)
        self.whatsapp_api_url = os.getenv('WHATSAPP_API_URL', '')
        self.whatsapp_token = os.getenv('WHATSAPP_TOKEN', '')
    
    def processar_template(self, template_conteudo, dados):
        """Processa o template substituindo as variáveis pelos dados"""
        try:
            return template_conteudo.format(**dados)
        except KeyError as e:
            raise ValueError(f"Variável não encontrada no template: {e}")
    
    def enviar_email(self, destinatario, assunto, conteudo):
        """Envia e-mail usando SMTP"""
        if not self.email_user or not self.email_password:
            raise ValueError("Configurações de e-mail não definidas")
        
        try:
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = destinatario
            msg['Subject'] = assunto
            
            # Adicionar conteúdo
            msg.attach(MIMEText(conteudo, 'plain', 'utf-8'))
            
            # Conectar ao servidor SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            
            # Enviar e-mail
            server.send_message(msg)
            server.quit()
            
            return {'success': True, 'message': 'E-mail enviado com sucesso'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def enviar_whatsapp(self, numero, conteudo):
        """Envia mensagem WhatsApp via API externa"""
        if not self.whatsapp_api_url or not self.whatsapp_token:
            # Simular envio para demonstração
            return {'success': True, 'message': 'WhatsApp simulado (configuração necessária)'}
        
        try:
            # Exemplo de integração com API do WhatsApp
            headers = {
                'Authorization': f'Bearer {self.whatsapp_token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'to': numero,
                'text': conteudo
            }
            
            response = requests.post(self.whatsapp_api_url, json=data, headers=headers)
            
            if response.status_code == 200:
                return {'success': True, 'message': 'WhatsApp enviado com sucesso'}
            else:
                return {'success': False, 'error': f'Erro na API: {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def enviar_notificacao(self, demanda, template_id, dados_extras=None):
        """Envia notificação baseada no template e demanda"""
        try:
            # Buscar template
            template = TemplateNotificacao.query.get(template_id)
            if not template or not template.ativo:
                return {'success': False, 'error': 'Template não encontrado ou inativo'}
            
            # Preparar dados para o template
            dados = {
                'professor_nome': demanda.professor,
                'tipo_conteudo': demanda.tipo_conteudo,
                'prazo_entrega': demanda.prazo_entrega.strftime('%d/%m/%Y') if demanda.prazo_entrega else '',
                'data_envio': demanda.data_envio.strftime('%d/%m/%Y') if demanda.data_envio else '',
                'roteiro_personalizado': dados_extras.get('roteiro', 'Roteiro será fornecido em breve.') if dados_extras else 'Roteiro será fornecido em breve.'
            }
            
            # Adicionar dados extras se fornecidos
            if dados_extras:
                dados.update(dados_extras)
            
            # Processar template
            conteudo_processado = self.processar_template(template.conteudo, dados)
            
            # Determinar destinatário baseado no professor
            destinatario = self.get_contato_professor(demanda.professor, template.tipo)
            if not destinatario:
                return {'success': False, 'error': f'Contato {template.tipo} não encontrado para o professor'}
            
            # Enviar notificação
            if template.tipo == 'email':
                assunto_processado = self.processar_template(template.assunto, dados) if template.assunto else 'Notificação Projeto Experts'
                resultado = self.enviar_email(destinatario, assunto_processado, conteudo_processado)
            elif template.tipo == 'whatsapp':
                resultado = self.enviar_whatsapp(destinatario, conteudo_processado)
            else:
                return {'success': False, 'error': 'Tipo de template não suportado'}
            
            # Registrar envio
            status = 'enviado' if resultado['success'] else 'erro'
            erro_detalhes = resultado.get('error') if not resultado['success'] else None
            
            notificacao = NotificacaoEnviada(
                demanda_id=demanda.id,
                template_id=template.id,
                tipo=template.tipo,
                destinatario=destinatario,
                status=status,
                erro_detalhes=erro_detalhes
            )
            
            db.session.add(notificacao)
            db.session.commit()
            
            return resultado
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_contato_professor(self, professor_nome, tipo_contato):
        """Retorna o contato do professor baseado no tipo (email ou whatsapp)"""
        # Mapeamento de professores e seus contatos
        # Em um sistema real, isso viria de um banco de dados
        contatos = {
            'Pedro Campos': {
                'email': 'pedro.campos@alfacon.com.br',
                'whatsapp': '+5511999999001'
            },
            'Pablo': {
                'email': 'pablo@alfacon.com.br',
                'whatsapp': '+5511999999002'
            },
            'Rafael Araújo': {
                'email': 'rafael.araujo@alfacon.com.br',
                'whatsapp': '+5511999999003'
            },
            'Samuel': {
                'email': 'samuel@alfacon.com.br',
                'whatsapp': '+5511999999004'
            },
            'Tiago Vidal': {
                'email': 'tiago.vidal@alfacon.com.br',
                'whatsapp': '+5511999999005'
            },
            'Rogério Dalvipa': {
                'email': 'rogerio.dalpiva@alfacon.com.br',
                'whatsapp': '+5511999999006'
            },
            'Lucas Fávero': {
                'email': 'lucas.favero@alfacon.com.br',
                'whatsapp': '+5511999999007'
            },
            'Pedro Canezin': {
                'email': 'pedro.canezin@alfacon.com.br',
                'whatsapp': '+5511999999008'
            },
            'Filipe Ávila': {
                'email': 'filipe.avila@alfacon.com.br',
                'whatsapp': '+5511999999009'
            },
            'João Paulo': {
                'email': 'joao.paulo@alfacon.com.br',
                'whatsapp': '+5511999999010'
            },
            'Heitor': {
                'email': 'heitor@alfacon.com.br',
                'whatsapp': '+5511999999011'
            }
        }
        
        professor_contatos = contatos.get(professor_nome, {})
        return professor_contatos.get(tipo_contato)

