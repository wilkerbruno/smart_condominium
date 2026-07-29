from condominio import db


class Seguranca(db.Model):
    __tablename__ = "seguranca"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    condominio_id = db.Column(db.Integer, db.ForeignKey("condominio.id"))
    tipo_registro = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_registro = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "condominio_id": self.condominio_id,
            "tipo_registro": self.tipo_registro,
            "descricao": self.descricao,
            "data_registro": self.data_registro.isoformat() if self.data_registro else None,
        }
