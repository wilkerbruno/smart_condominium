"""
funcionario_model.py
=====================
PESSOA funcionário — identidade única (login + CPF). Os condomínios onde
essa pessoa trabalha (e o cargo/salário em cada um) ficam em
`funcionario_condominio` (relação `condominios`), permitindo a mesma
pessoa atuar (ex.: como síndico) em mais de um condomínio.
"""
from condominio import db


class Funcionario(db.Model):
    __tablename__ = "funcionario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(80), unique=True)
    documento_identidade = db.Column(db.String(20), unique=True)  # CPF — chave de deduplicação
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    senha_hash = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, nullable=False, default=False)

    condominios = db.relationship(
        "FuncionarioCondominio", backref="funcionario", lazy=True, cascade="all, delete-orphan"
    )
    escalas = db.relationship("Escala", backref="funcionario", lazy=True, cascade="all, delete-orphan")

    def to_dict(self, incluir_condominios=False):
        data = {
            "id": self.id,
            "nome": self.nome,
            "usuario": self.usuario,
            "documento_identidade": self.documento_identidade,
            "telefone": self.telefone,
            "email": self.email,
            "ativo": bool(self.ativo),
        }
        if incluir_condominios:
            data["condominios"] = [c.to_dict() for c in self.condominios if c.ativo]
        return data

    def to_dict_publico(self):
        """Dados pessoais SEM cargo/salário/condomínio — usado na busca por
        CPF ao cadastrar a mesma pessoa em outro condomínio."""
        return {
            "id": self.id,
            "nome": self.nome,
            "documento_identidade": self.documento_identidade,
            "telefone": self.telefone,
            "email": self.email,
            "usuario": self.usuario,
        }

    def __repr__(self):
        return f"<Funcionario {self.nome}>"
