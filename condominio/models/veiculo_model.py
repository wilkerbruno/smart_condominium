from condominio import db


class Veiculo(db.Model):
    __tablename__ = 'veiculo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(20), nullable=False)
    nome = db.Column(db.String(20), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    modelo = db.Column(db.String(20), nullable=False)
    placa = db.Column(db.String(20), nullable=False, unique=True)
    cor = db.Column(db.String(20), nullable=False)

    def __init__(self, tipo, nome, ano, modelo, placa, cor):
        self.tipo = tipo
        self.nome = nome
        self.ano = ano
        self.modelo = modelo
        self.placa = placa
        self.cor = cor