from condominio import db


class Escala(db.Model):
    __tablename__ = "escala"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionario.id", ondelete="CASCADE"), nullable=False)
    tipo = db.Column(db.String(20), nullable=False, default="padrao")  # padrao | especifico
    dia_semana = db.Column(db.SmallInteger, nullable=False)  # 0=Domingo ... 6=Sabado
    turno = db.Column(db.String(20))  # manha | tarde | noite | folga | ferias
    hora_entrada = db.Column(db.String(5))
    hora_saida = db.Column(db.String(5))
    observacao = db.Column(db.String(255))
    semana_ref = db.Column(db.Date)
    criado_em = db.Column(db.DateTime)
    atualizado_em = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "funcionario_id": self.funcionario_id,
            "tipo": self.tipo,
            "dia_semana": self.dia_semana,
            "turno": self.turno,
            "hora_entrada": self.hora_entrada,
            "hora_saida": self.hora_saida,
            "observacao": self.observacao,
            "semana_ref": self.semana_ref.isoformat() if self.semana_ref else None,
        }

    def __repr__(self):
        return f"<Escala func={self.funcionario_id} dia={self.dia_semana}>"
