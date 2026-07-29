from condominio import db


class Financeiro(db.Model):
    __tablename__ = "financeiro"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    condominio_id = db.Column(db.Integer, db.ForeignKey("condominio.id"))
    tipo_transacao = db.Column(db.String(20), nullable=False)  # receita | despesa
    descricao_transacao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    data_transacao = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "condominio_id": self.condominio_id,
            "tipo_transacao": self.tipo_transacao,
            "descricao_transacao": self.descricao_transacao,
            "valor": float(self.valor) if self.valor is not None else None,
            "data_transacao": self.data_transacao.isoformat() if self.data_transacao else None,
        }
