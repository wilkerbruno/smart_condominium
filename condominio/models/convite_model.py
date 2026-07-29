from datetime import datetime, timedelta

from condominio import db


class Convite(db.Model):
    """
    Armazena tokens de confirmação de e-mail para funcionários e moradores.
    Após o usuário clicar no link e definir a senha, o token é marcado como 'usado'.
    """
    __tablename__ = 'convite'

    id        = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    tipo      = db.Column(db.String(20),  nullable=False)   # 'funcionario' | 'morador'
    ref_id    = db.Column(db.Integer,     nullable=False)   # ID do funcionario/morador
    email     = db.Column(db.String(100), nullable=False)
    nome      = db.Column(db.String(100), nullable=False)
    token     = db.Column(db.String(100), nullable=False, unique=True)
    usado     = db.Column(db.Boolean,     nullable=False, default=False)
    criado_em = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)
    expira_em = db.Column(db.DateTime,    nullable=False)

    def __init__(self, tipo, ref_id, email, nome, token, dias_validade=7):
        self.tipo      = tipo
        self.ref_id    = ref_id
        self.email     = email
        self.nome      = nome
        self.token     = token
        self.criado_em = datetime.utcnow()
        self.expira_em = datetime.utcnow() + timedelta(days=dias_validade)

    @property
    def expirado(self):
        return datetime.utcnow() > self.expira_em

    @property
    def valido(self):
        return not self.usado and not self.expirado

    def __repr__(self):
        return f'<Convite {self.tipo} #{self.ref_id} usado={self.usado}>'