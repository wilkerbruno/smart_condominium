"""
morador_unidade_model.py
=========================
Tabela de associação: liga uma PESSOA (morador, identidade única — login,
CPF) a uma UNIDADE (apartamento/casa) de um condomínio. Uma mesma pessoa
pode ter vários vínculos (apartamentos em condomínios diferentes, ou até
no mesmo condomínio).
"""
from datetime import datetime

from condominio import db


class MoradorUnidade(db.Model):
    __tablename__ = "morador_unidade"
    __table_args__ = (db.UniqueConstraint("morador_id", "unidade_id", name="uq_morador_unidade"),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    morador_id = db.Column(db.Integer, db.ForeignKey("morador.id", ondelete="CASCADE"), nullable=False)
    unidade_id = db.Column(db.Integer, db.ForeignKey("unidade.id", ondelete="CASCADE"), nullable=False)
    relacao_unidade = db.Column(db.String(50), nullable=False, default="Proprietário")
    veiculo_placa = db.Column(db.String(20))
    veiculo_modelo = db.Column(db.String(50))
    veiculo_cor = db.Column(db.String(50))
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    unidade = db.relationship("Unidade", lazy=True)

    def to_dict(self, incluir_condominio=True):
        unidade = self.unidade
        data = {
            "vinculo_id": self.id,
            "morador_id": self.morador_id,
            "unidade": unidade.to_dict() if unidade else None,
            "relacao_unidade": self.relacao_unidade,
            "veiculo_placa": self.veiculo_placa,
            "veiculo_modelo": self.veiculo_modelo,
            "veiculo_cor": self.veiculo_cor,
            "ativo": bool(self.ativo),
        }
        if incluir_condominio and unidade and unidade.condominio:
            data["condominio"] = unidade.condominio.to_dict()
        return data
