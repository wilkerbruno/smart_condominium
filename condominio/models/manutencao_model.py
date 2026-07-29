from condominio import db


class ManutencaoServico(db.Model):
    __tablename__ = "manutencaoservicos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    condominio_id = db.Column(db.Integer, db.ForeignKey("condominio.id"))
    descricao_servico = db.Column(db.Text, nullable=False)
    data_servico = db.Column(db.Date, nullable=False)
    custo = db.Column(db.Numeric(10, 2))
    prestador_servico = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "condominio_id": self.condominio_id,
            "descricao_servico": self.descricao_servico,
            "data_servico": self.data_servico.isoformat() if self.data_servico else None,
            "custo": float(self.custo) if self.custo is not None else None,
            "prestador_servico": self.prestador_servico,
        }
