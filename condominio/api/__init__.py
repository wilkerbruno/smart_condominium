"""
condominio/api — API REST (JSON + JWT) do Smart Condominium.

Consumida pelo site (opcional) e pelo app mobile (React Native / Expo).
Todas as rotas ficam sob o prefixo /api/v1 (definido no registro do
blueprint em condominio/__init__.py).
"""
from flask import Blueprint, jsonify

from .auth import auth_bp
from .moradores import moradores_bp
from .funcionarios import funcionarios_bp
from .pessoas import pessoas_bp
from .escalas import escalas_bp
from .convites import convites_bp
from .crud_generico import criar_blueprint_crud

from condominio.models.condominio_model import Condominio
from condominio.models.unidade_model import Unidade
from condominio.models.areacomum_model import AreaComum
from condominio.models.comunicacao_model import Comunicacao
from condominio.models.documentolegal_model import DocumentoLegal
from condominio.models.financeiro_model import Financeiro
from condominio.models.manutencao_model import ManutencaoServico
from condominio.models.seguranca_model import Seguranca

api_bp = Blueprint("api", __name__)

api_bp.register_blueprint(auth_bp, url_prefix="/auth")
api_bp.register_blueprint(moradores_bp, url_prefix="/moradores")
api_bp.register_blueprint(funcionarios_bp, url_prefix="/funcionarios")
api_bp.register_blueprint(pessoas_bp, url_prefix="/pessoas")
api_bp.register_blueprint(escalas_bp, url_prefix="/escalas")
api_bp.register_blueprint(convites_bp, url_prefix="/convites")

api_bp.register_blueprint(
    criar_blueprint_crud(
        "condominios", Condominio,
        campos_obrigatorios=("nome", "endereco", "cidade", "estado", "cep", "celular"),
        campos_permitidos=("nome", "numero", "endereco", "cidade", "estado", "cep",
                            "telefone", "celular", "email", "sindico_nome",
                            "sindico_telefone", "sindico_email", "regras_regulamentos"),
    ),
    url_prefix="/condominios",
)
api_bp.register_blueprint(
    criar_blueprint_crud(
        "unidades", Unidade,
        campos_obrigatorios=("numero_unidade", "proprietario_residente", "tipo_unidade", "status"),
        campos_permitidos=("condominio_id", "numero_unidade", "proprietario_residente",
                            "telefone_proprietario", "email_proprietario", "tipo_unidade",
                            "status", "area"),
    ),
    url_prefix="/unidades",
)
api_bp.register_blueprint(
    criar_blueprint_crud(
        "areas_comuns", AreaComum,
        campos_obrigatorios=("descricao",),
        campos_permitidos=("condominio_id", "descricao", "regras_uso"),
    ),
    url_prefix="/areas-comuns",
)
api_bp.register_blueprint(
    criar_blueprint_crud(
        "comunicados", Comunicacao,
        campos_obrigatorios=("titulo", "conteudo", "data_envio"),
        campos_permitidos=("condominio_id", "titulo", "conteudo", "data_envio"),
        cargos_escrita=("sindico", "administrador", "porteiro"),
    ),
    url_prefix="/comunicados",
)
api_bp.register_blueprint(
    criar_blueprint_crud(
        "documentos", DocumentoLegal,
        campos_obrigatorios=("tipo_documento",),
        campos_permitidos=("condominio_id", "tipo_documento", "descricao"),
    ),
    url_prefix="/documentos",
)
api_bp.register_blueprint(
    criar_blueprint_crud(
        "financeiro", Financeiro,
        campos_obrigatorios=("tipo_transacao", "descricao_transacao", "valor", "data_transacao"),
        campos_permitidos=("condominio_id", "tipo_transacao", "descricao_transacao",
                            "valor", "data_transacao"),
    ),
    url_prefix="/financeiro",
)
api_bp.register_blueprint(
    criar_blueprint_crud(
        "manutencoes", ManutencaoServico,
        campos_obrigatorios=("descricao_servico", "data_servico"),
        campos_permitidos=("condominio_id", "descricao_servico", "data_servico",
                            "custo", "prestador_servico"),
    ),
    url_prefix="/manutencoes",
)
api_bp.register_blueprint(
    criar_blueprint_crud(
        "seguranca", Seguranca,
        campos_obrigatorios=("tipo_registro", "descricao", "data_registro"),
        campos_permitidos=("condominio_id", "tipo_registro", "descricao", "data_registro"),
        cargos_escrita=("sindico", "administrador", "porteiro", "seguranca"),
    ),
    url_prefix="/seguranca",
)


@api_bp.route("/saude", methods=["GET"])
def saude():
    """Healthcheck simples para monitoramento (EasyPanel, uptime checks, etc.)."""
    return jsonify({"sucesso": True, "servico": "smart-condominium-api", "status": "online"})
