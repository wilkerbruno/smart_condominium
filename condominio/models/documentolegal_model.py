from condominio import db


class DocumentoLegal(db.Model):
    __tablename__ = "documentolegal"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    condominio_id = db.Column(db.Integer, db.ForeignKey("condominio.id"))
    tipo_documento = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "condominio_id": self.condominio_id,
            "tipo_documento": self.tipo_documento,
            "descricao": self.descricao,
        }
