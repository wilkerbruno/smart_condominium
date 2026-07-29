"""
morador_model.py
=================
PESSOA morador — identidade única (login + CPF). Os apartamentos onde
essa pessoa mora ficam em `morador_unidade` (relação `unidades`), o que
permite a mesma pessoa ter unidades em condomínios diferentes sem
duplicar cadastro.
"""
from condominio import db


class Morador(db.Model):
    __tablename__ = "morador"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(80), unique=True)
    documento_identidade = db.Column(db.String(20), unique=True)  # CPF — chave de deduplicação
    data_nascimento = db.Column(db.Date)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    senha_hash = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, nullable=False, default=False)

    unidades = db.relationship(
        "MoradorUnidade", backref="morador", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self, incluir_unidades=False):
        data = {
            "id": self.id,
            "nome": self.nome,
            "usuario": self.usuario,
            "documento_identidade": self.documento_identidade,
            "data_nascimento": self.data_nascimento.isoformat() if self.data_nascimento else None,
            "telefone": self.telefone,
            "email": self.email,
            "ativo": bool(self.ativo),
        }
        if incluir_unidades:
            data["unidades"] = [
                v.to_dict() for v in self.unidades if v.ativo
            ]
        return data

    def to_dict_publico(self):
        """Dados pessoais SEM nada de apartamento — usado na busca por CPF
        ao cadastrar a mesma pessoa em outro condomínio."""
        return {
            "id": self.id,
            "nome": self.nome,
            "documento_identidade": self.documento_identidade,
            "data_nascimento": self.data_nascimento.isoformat() if self.data_nascimento else None,
            "telefone": self.telefone,
            "email": self.email,
            "usuario": self.usuario,
        }

    def __repr__(self):
        return f"<Morador {self.nome}>"
