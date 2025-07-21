from src.db import db

class Professor(db.Model):
    __tablename__ = 'professores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    disciplinas = db.Column(db.String(255), nullable=True)
    instagram = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    whatsapp = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<Professor {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'disciplinas': self.disciplinas,
            'instagram': self.instagram,
            'email': self.email,
            'whatsapp': self.whatsapp
        }
