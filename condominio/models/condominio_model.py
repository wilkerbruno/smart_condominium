from condominio import db


class Condominio(db.Model):
    __tablename__ = "condominio"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    numero = db.Column(db.String(10), nullable=False, default="")
    endereco = db.Column(db.String(255), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    cep = db.Column(db.String(20), nullable=False)
    telefone = db.Column(db.String(20))
    celular = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    sindico_nome = db.Column(db.String(100))
    sindico_telefone = db.Column(db.String(20))
    sindico_email = db.Column(db.String(100))
    regras_regulamentos = db.Column(db.Text)

    unidades = db.relationship("Unidade", backref="condominio", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "numero": self.numero,
            "endereco": self.endereco,
            "cidade": self.cidade,
            "estado": self.estado,
            "cep": self.cep,
            "telefone": self.telefone,
            "celular": self.celular,
            "email": self.email,
            "sindico_nome": self.sindico_nome,
            "sindico_telefone": self.sindico_telefone,
            "sindico_email": self.sindico_email,
            "regras_regulamentos": self.regras_regulamentos,
        }

    def __repr__(self):
        return f"<Condominio {self.nome}>"
