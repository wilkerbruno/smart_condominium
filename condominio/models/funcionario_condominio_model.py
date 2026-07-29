"""
funcionario_condominio_model.py
=================================
Tabela de associação: liga uma PESSOA (funcionário, identidade única —
login, CPF) a um CONDOMÍNIO onde ela trabalha, com o cargo e demais
dados daquele vínculo específico. Um síndico/funcionário pode atuar em
mais de um condomínio, cada um com seu próprio cargo/salário/horário.
"""
from datetime import datetime

from condominio import db


class FuncionarioCondominio(db.Model):
    __tablename__ = "funcionario_condominio"
    __table_args__ = (db.UniqueConstraint("funcionario_id", "condominio_id", name="uq_funcionario_condominio"),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionario.id", ondelete="CASCADE"), nullable=False)
    condominio_id = db.Column(db.Integer, db.ForeignKey("condominio.id", ondelete="CASCADE"), nullable=False)
    cargo = db.Column(db.String(50), nullable=False)
    horario_trabalho = db.Column(db.String(100))
    salario_funcionario = db.Column(db.Float, nullable=False, default=0)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    condominio = db.relationship("Condominio", lazy=True)

    def to_dict(self, incluir_salario=False):
        data = {
            "vinculo_id": self.id,
            "funcionario_id": self.funcionario_id,
            "condominio": self.condominio.to_dict() if self.condominio else None,
            "cargo": self.cargo,
            "horario_trabalho": self.horario_trabalho,
            "ativo": bool(self.ativo),
        }
        if incluir_salario:
            data["salario_funcionario"] = self.salario_funcionario
        return data
