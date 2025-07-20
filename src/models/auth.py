from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from src.models.user import db

class Coordenador(UserMixin, db.Model):
    __tablename__ = 'coordenadores'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nome': self.nome,
            'ativo': self.ativo
        }
    
    @staticmethod
    def create_default_user():
        """Cria um usuário padrão se não existir nenhum coordenador"""
        if not Coordenador.query.first():
            coordenador = Coordenador(
                username='admin',
                email='admin@alfacon.com.br',
                nome='Administrador'
            )
            coordenador.set_password('admin123')  # Senha padrão - deve ser alterada
            db.session.add(coordenador)
            db.session.commit()
            return coordenador
        return None

