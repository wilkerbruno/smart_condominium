from condominio import db


class AreaComum(db.Model):
    __tablename__ = "areacomum"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    condominio_id = db.Column(db.Integer, db.ForeignKey("condominio.id"))
    descricao = db.Column(db.String(255), nullable=False)
    regras_uso = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "condominio_id": self.condominio_id,
            "descricao": self.descricao,
            "regras_uso": self.regras_uso,
        }
