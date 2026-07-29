from condominio import db


class Comunicacao(db.Model):
    __tablename__ = "comunicacao"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    condominio_id = db.Column(db.Integer, db.ForeignKey("condominio.id"))
    titulo = db.Column(db.String(255), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    data_envio = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "condominio_id": self.condominio_id,
            "titulo": self.titulo,
            "conteudo": self.conteudo,
            "data_envio": self.data_envio.isoformat() if self.data_envio else None,
        }
