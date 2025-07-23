import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_login import LoginManager
from src.db import db
from src.models.user import User
from src.models.demanda import Demanda
from src.models.auth import Coordenador
from src.models.template import TemplateNotificacao
from src.routes.user import user_bp
from src.routes.dashboard import dashboard_bp
from src.routes.auth import auth_bp
from src.routes.notification import notification_bp
from src.routes.professor import professor_bp

# Criação da aplicação
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-dev-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise RuntimeError("DATABASE_URL not set in environment variables.")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return Coordenador.query.get(int(user_id))

# Blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(dashboard_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(notification_bp, url_prefix='/api/notifications')
app.register_blueprint(professor_bp, url_prefix='/api/professores')

# Inicialização do banco
with app.app_context():
    db.create_all()
    Coordenador.create_default_user()
    TemplateNotificacao.create_default_templates()

# Frontend SPA
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    full_path = os.path.join(static_folder_path, path)
    index_path = os.path.join(static_folder_path, 'index.html')

    if path and os.path.exists(full_path):
        return send_from_directory(static_folder_path, path)
    elif os.path.exists(index_path):
        return send_from_directory(static_folder_path, 'index.html')
    else:
        return "index.html not found", 404

# Execução local
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
