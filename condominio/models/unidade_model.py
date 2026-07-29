from condominio import db


class Unidade(db.Model):
    __tablename__ = "unidade"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    condominio_id = db.Column(db.Integer, db.ForeignKey("condominio.id"))
    numero_unidade = db.Column(db.String(20), nullable=False)
    proprietario_residente = db.Column(db.String(100), nullable=False)
    telefone_proprietario = db.Column(db.String(20))
    email_proprietario = db.Column(db.String(100))
    tipo_unidade = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    area = db.Column(db.Numeric(10, 2))

    def to_dict(self):
        return {
            "id": self.id,
            "condominio_id": self.condominio_id,
            "numero_unidade": self.numero_unidade,
            "proprietario_residente": self.proprietario_residente,
            "telefone_proprietario": self.telefone_proprietario,
            "email_proprietario": self.email_proprietario,
            "tipo_unidade": self.tipo_unidade,
            "status": self.status,
            "area": float(self.area) if self.area is not None else None,
        }

    def __repr__(self):
        return f"<Unidade {self.numero_unidade}>"
