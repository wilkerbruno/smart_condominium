import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

path = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

app.config.from_object("config")
app.secret_key = app.config["SECRET_KEY"]

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# CORS liberado apenas para /api/* — o app mobile (Expo) e eventuais SPAs
# chamam a API a partir de outra origem. As páginas SSR do site não
# precisam de CORS pois são renderizadas no mesmo domínio.
CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}}, supports_credentials=True)

# ── Views web (SSR) existentes ──────────────────────────────────
from .views.views import *
from .views.condominio_views import *
from .views.veiculo_views import *
from .views.morador_views import *
from .views.invite_views import *          # sistema de convites (fluxo web)

# ── Models ───────────────────────────────────────────────────────
from .models.veiculo_model import Veiculo
from .models.morador_model import Morador
from .models.morador_unidade_model import MoradorUnidade
from .models.funcionario_model import Funcionario
from .models.funcionario_condominio_model import FuncionarioCondominio
from .models.condominio_model import Condominio
from .models.unidade_model import Unidade
from .models.convite_model import Convite
from .models.escala_model import Escala
from .models.areacomum_model import AreaComum
from .models.comunicacao_model import Comunicacao
from .models.documentolegal_model import DocumentoLegal
from .models.financeiro_model import Financeiro
from .models.manutencao_model import ManutencaoServico
from .models.seguranca_model import Seguranca

# ── API REST (consumida pelo app mobile React Native / Expo) ─────
from .api import api_bp
app.register_blueprint(api_bp, url_prefix="/api/v1")
