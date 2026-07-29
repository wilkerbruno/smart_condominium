"""
db_raw.py
=========
Helper único para conexões pymysql "cruas" (fora do ORM), usado pelas
views legadas que ainda fazem SQL manual. Lê a configuração do
`app.config`, que por sua vez vem de variáveis de ambiente — nunca
credenciais hardcoded no código-fonte.
"""
import pymysql

from condominio import app


def get_conn():
    """Retorna uma conexão pymysql configurada via variáveis de ambiente."""
    return pymysql.connect(
        host=app.config["DB_HOST"],
        port=app.config["DB_PORT"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        db=app.config["DB_NAME"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
