from src.db import db
from datetime import datetime

class Demanda(db.Model):
    __tablename__ = 'demandas'
    
    id = db.Column(db.Integer, primary_key=True)
    professor = db.Column(db.String(100), nullable=False)
    disciplina = db.Column(db.String(100), nullable=True)
    tipo_conteudo = db.Column(db.String(50), nullable=False)
    data_envio = db.Column(db.Date, nullable=False, default=datetime.now().date())
    prazo_entrega = db.Column(db.Date, nullable=False)
    data_entrega = db.Column(db.Date, nullable=True)
    material_entregue = db.Column(db.String(10), nullable=True)
    conformidade_roteiro = db.Column(db.String(10), nullable=True)
    plataforma_publicacao = db.Column(db.String(50), nullable=True)

    # Métricas do Instagram do Professor
    alcance_professor = db.Column(db.Integer, nullable=True)
    impressoes_professor = db.Column(db.Integer, nullable=True)
    curtidas_professor = db.Column(db.Integer, nullable=True)
    comentarios_professor = db.Column(db.Integer, nullable=True)
    compartilhamentos_professor = db.Column(db.Integer, nullable=True)
    salvos_professor = db.Column(db.Integer, nullable=True)
    visualizacoes_professor = db.Column(db.Integer, nullable=True)

    # Métricas do Instagram do AlfaCon
    alcance_alfacon = db.Column(db.Integer, nullable=True)
    impressoes_alfacon = db.Column(db.Integer, nullable=True)
    curtidas_alfacon = db.Column(db.Integer, nullable=True)
    comentarios_alfacon = db.Column(db.Integer, nullable=True)
    compartilhamentos_alfacon = db.Column(db.Integer, nullable=True)
    salvos_alfacon = db.Column(db.Integer, nullable=True)
    visualizacoes_alfacon = db.Column(db.Integer, nullable=True)

    trafego_gerado = db.Column(db.String(200), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'professor': self.professor,
            'disciplina': self.disciplina,
            'tipo_conteudo': self.tipo_conteudo,
            'data_envio': self.data_envio.isoformat() if self.data_envio else None,
            'prazo_entrega': self.prazo_entrega.isoformat() if self.prazo_entrega else None,
            'data_entrega': self.data_entrega.isoformat() if self.data_entrega else None,
            'material_entregue': self.material_entregue,
            'conformidade_roteiro': self.conformidade_roteiro,
            'plataforma_publicacao': self.plataforma_publicacao,
            'alcance_professor': self.alcance_professor,
            'impressoes_professor': self.impressoes_professor,
            'curtidas_professor': self.curtidas_professor,
            'comentarios_professor': self.comentarios_professor,
            'compartilhamentos_professor': self.compartilhamentos_professor,
            'salvos_professor': self.salvos_professor,
            'visualizacoes_professor': self.visualizacoes_professor,
            'alcance_alfacon': self.alcance_alfacon,
            'impressoes_alfacon': self.impressoes_alfacon,
            'curtidas_alfacon': self.curtidas_alfacon,
            'comentarios_alfacon': self.comentarios_alfacon,
            'compartilhamentos_alfacon': self.compartilhamentos_alfacon,
            'salvos_alfacon': self.salvos_alfacon,
            'visualizacoes_alfacon': self.visualizacoes_alfacon,
            'trafego_gerado': self.trafego_gerado,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }