"""
config.py
=========
Configuração da aplicação lida inteiramente de variáveis de ambiente.
NENHUM segredo (senha de banco, chaves) deve ficar hardcoded aqui ou em
qualquer outro arquivo versionado — use o `.env` (local) ou as variáveis
de ambiente do EasyPanel (produção).

Veja `.env.example` para a lista completa de variáveis esperadas.
"""
import os
from datetime import timedelta

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


def _env(key, default=None, required=False):
    val = os.environ.get(key, default)
    if required and (val is None or val == ""):
        raise RuntimeError(
            f"Variável de ambiente obrigatória não definida: {key}. "
            f"Copie .env.example para .env e preencha os valores."
        )
    return val


# ── Segurança ────────────────────────────────────────────────────
SECRET_KEY = _env("SECRET_KEY", required=True)
JWT_SECRET_KEY = _env("JWT_SECRET_KEY", required=True)
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(_env("JWT_ACCESS_TOKEN_HOURS", "8")))
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(_env("JWT_REFRESH_TOKEN_DAYS", "30")))
JWT_TOKEN_LOCATION = ["headers"]

# ── Banco de dados ───────────────────────────────────────────────
DB_HOST = _env("DB_HOST", required=True)
DB_PORT = int(_env("DB_PORT", "3306"))
DB_USER = _env("DB_USER", required=True)
DB_PASSWORD = _env("DB_PASSWORD", required=True)
DB_NAME = _env("DB_NAME", required=True)

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 280}

# ── CORS (necessário para o app mobile / Expo consumir a API) ────
CORS_ORIGINS = [o.strip() for o in _env("CORS_ORIGINS", "*").split(",")]

# ── Ambiente ─────────────────────────────────────────────────────
ENV = _env("FLASK_ENV", "production")
DEBUG = ENV == "development"
