"""
migrate_pessoa_condominio.py
=============================
Migration: separa PESSOA (login/CPF) de VÍNCULO (unidade/condomínio),
permitindo que a mesma pessoa seja morador/funcionário em mais de um
condomínio sem duplicar cadastro.

O que faz (idempotente — pode rodar quantas vezes precisar):
  1. Cria a tabela `morador_unidade` (pessoa <-> unidade).
  2. Cria a tabela `funcionario_condominio` (pessoa <-> condomínio).
  3. Adiciona `documento_identidade` (CPF) em `funcionario`, se não existir.
  4. Copia os vínculos que já existem hoje (morador.unidade_id,
     funcionario.condominio_id/cargo/...) para as novas tabelas.
  5. Tenta criar índices UNIQUE em documento_identidade — se houver CPFs
     duplicados/vazios em conflito, ela avisa e você decide o que fazer
     (não quebra a migration).

IMPORTANTE: as colunas antigas (morador.unidade_id, morador.veiculo_*,
funcionario.condominio_id, funcionario.cargo, etc.) NÃO são apagadas por
segurança. O código novo não usa mais elas. Depois de validar que está
tudo certo em produção, você pode rodar um DROP COLUMN manual.

Uso:
    python migrate_pessoa_condominio.py
"""
import os
import sys

import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host":     os.environ["DB_HOST"],
    "port":     int(os.environ.get("DB_PORT", "3306")),
    "user":     os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "db":       os.environ["DB_NAME"],
    "charset":  "utf8mb4",
}


def _get_conn():
    return pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)


def _sep(titulo=""):
    linha = "═" * 62
    print(f"\n{linha}")
    if titulo:
        print(f"  {titulo}")
        print(linha)


def _tabela_existe(cur, tabela):
    cur.execute(
        "SELECT COUNT(*) AS n FROM information_schema.TABLES "
        "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s",
        (DB_CONFIG["db"], tabela),
    )
    return cur.fetchone()["n"] > 0


def _coluna_existe(cur, tabela, coluna):
    cur.execute(
        "SELECT COUNT(*) AS n FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s",
        (DB_CONFIG["db"], tabela, coluna),
    )
    return cur.fetchone()["n"] > 0


def _indice_existe(cur, tabela, nome_idx):
    cur.execute(
        "SELECT COUNT(*) AS n FROM information_schema.STATISTICS "
        "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND INDEX_NAME = %s",
        (DB_CONFIG["db"], tabela, nome_idx),
    )
    return cur.fetchone()["n"] > 0


DDL_MORADOR_UNIDADE = """
CREATE TABLE IF NOT EXISTS `morador_unidade` (
    `id`               INT(11)      NOT NULL AUTO_INCREMENT,
    `morador_id`       INT(11)      NOT NULL,
    `unidade_id`       INT(11)      NOT NULL,
    `relacao_unidade`  VARCHAR(50)  NOT NULL DEFAULT 'Proprietário',
    `veiculo_placa`    VARCHAR(20)  DEFAULT NULL,
    `veiculo_modelo`   VARCHAR(50)  DEFAULT NULL,
    `veiculo_cor`      VARCHAR(50)  DEFAULT NULL,
    `ativo`            TINYINT(1)   NOT NULL DEFAULT 1,
    `criado_em`        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_morador_unidade` (`morador_id`, `unidade_id`),
    KEY `idx_morador` (`morador_id`),
    KEY `idx_unidade` (`unidade_id`),
    CONSTRAINT `fk_morador_unidade_morador`
        FOREIGN KEY (`morador_id`) REFERENCES `morador` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_morador_unidade_unidade`
        FOREIGN KEY (`unidade_id`) REFERENCES `unidade` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
"""

DDL_FUNCIONARIO_CONDOMINIO = """
CREATE TABLE IF NOT EXISTS `funcionario_condominio` (
    `id`                   INT(11)       NOT NULL AUTO_INCREMENT,
    `funcionario_id`       INT(11)       NOT NULL,
    `condominio_id`        INT(11)       NOT NULL,
    `cargo`                VARCHAR(50)   NOT NULL,
    `horario_trabalho`     VARCHAR(100)  DEFAULT NULL,
    `salario_funcionario`  DOUBLE        NOT NULL DEFAULT 0,
    `ativo`                TINYINT(1)    NOT NULL DEFAULT 1,
    `criado_em`            DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_funcionario_condominio` (`funcionario_id`, `condominio_id`),
    KEY `idx_funcionario` (`funcionario_id`),
    KEY `idx_condominio` (`condominio_id`),
    CONSTRAINT `fk_funcionario_condominio_funcionario`
        FOREIGN KEY (`funcionario_id`) REFERENCES `funcionario` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_funcionario_condominio_condominio`
        FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
"""


def criar_tabelas_associacao(conn):
    _sep("1/5 — Criando tabelas de associação")
    with conn.cursor() as cur:
        cur.execute(DDL_MORADOR_UNIDADE)
        print("   ✅ Tabela 'morador_unidade' — OK")
        cur.execute(DDL_FUNCIONARIO_CONDOMINIO)
        print("   ✅ Tabela 'funcionario_condominio' — OK")
    conn.commit()


def adicionar_documento_funcionario(conn):
    _sep("2/5 — Adicionando CPF ao funcionário")
    with conn.cursor() as cur:
        if _coluna_existe(cur, "funcionario", "documento_identidade"):
            print("   ⏭  Coluna 'funcionario.documento_identidade' já existe.")
        else:
            cur.execute(
                "ALTER TABLE `funcionario` "
                "ADD COLUMN `documento_identidade` VARCHAR(20) DEFAULT NULL "
                "COMMENT 'CPF — usado para deduplicar cadastro entre condomínios' "
                "AFTER `nome`"
            )
            conn.commit()
            print("   ✅ Coluna 'funcionario.documento_identidade' adicionada.")


def migrar_moradores(conn):
    _sep("3/5 — Migrando vínculos de morador -> unidade")
    with conn.cursor() as cur:
        if not _coluna_existe(cur, "morador", "unidade_id"):
            print("   ⏭  'morador.unidade_id' não existe mais — nada a migrar.")
            return
        cur.execute(
            "SELECT id, unidade_id, relacao_unidade, veiculo_placa, "
            "       veiculo_modelo, veiculo_cor "
            "FROM morador WHERE unidade_id IS NOT NULL"
        )
        linhas = cur.fetchall()
        migrados = 0
        for r in linhas:
            cur.execute(
                "INSERT IGNORE INTO morador_unidade "
                "(morador_id, unidade_id, relacao_unidade, veiculo_placa, veiculo_modelo, veiculo_cor, ativo) "
                "VALUES (%s, %s, %s, %s, %s, %s, 1)",
                (r["id"], r["unidade_id"], r["relacao_unidade"] or "Proprietário",
                 r["veiculo_placa"], r["veiculo_modelo"], r["veiculo_cor"]),
            )
            migrados += cur.rowcount
        conn.commit()
        print(f"   ✅ {migrados} vínculo(s) de unidade migrado(s) ({len(linhas)} morador(es) com unidade_id).")


def migrar_funcionarios(conn):
    _sep("4/5 — Migrando vínculos de funcionário -> condomínio")
    with conn.cursor() as cur:
        if not _coluna_existe(cur, "funcionario", "condominio_id"):
            print("   ⏭  'funcionario.condominio_id' não existe mais — nada a migrar.")
            return
        cur.execute(
            "SELECT id, condominio_id, cargo, horario_trabalho, salario_funcionario "
            "FROM funcionario WHERE condominio_id IS NOT NULL"
        )
        linhas = cur.fetchall()
        migrados = 0
        for r in linhas:
            cur.execute(
                "INSERT IGNORE INTO funcionario_condominio "
                "(funcionario_id, condominio_id, cargo, horario_trabalho, salario_funcionario, ativo) "
                "VALUES (%s, %s, %s, %s, %s, 1)",
                (r["id"], r["condominio_id"], r["cargo"], r["horario_trabalho"],
                 r["salario_funcionario"] or 0),
            )
            migrados += cur.rowcount
        conn.commit()
        print(f"   ✅ {migrados} vínculo(s) de condomínio migrado(s) ({len(linhas)} funcionário(s)).")


def criar_indices_documento(conn):
    _sep("5/5 — Tentando criar índices UNIQUE em documento_identidade")
    for tabela in ("morador", "funcionario"):
        idx_name = f"uq_{tabela}_documento"
        with conn.cursor() as cur:
            if _indice_existe(cur, tabela, idx_name):
                print(f"   ⏭  Índice '{idx_name}' já existe.")
                continue
            # Detecta duplicatas antes de tentar (não trava a migration se houver)
            cur.execute(
                f"SELECT documento_identidade, COUNT(*) AS n FROM `{tabela}` "
                f"WHERE documento_identidade IS NOT NULL AND documento_identidade != '' "
                f"GROUP BY documento_identidade HAVING n > 1"
            )
            duplicados = cur.fetchall()
            if duplicados:
                print(f"   ⚠️  {len(duplicados)} CPF(s) duplicado(s) em '{tabela}' — "
                      f"índice UNIQUE não criado. Resolva manualmente e rode de novo:")
                for d in duplicados[:10]:
                    print(f"        • {d['documento_identidade']}  ({d['n']}x)")
                continue
            try:
                cur.execute(f"ALTER TABLE `{tabela}` ADD UNIQUE KEY `{idx_name}` (`documento_identidade`)")
                conn.commit()
                print(f"   ✅ Índice UNIQUE '{idx_name}' criado.")
            except pymysql.MySQLError as e:
                print(f"   ⚠️  Não foi possível criar '{idx_name}': {e}")


def relaxar_colunas_legado(conn):
    """
    Colunas antigas que ficaram sem uso no código novo (cargo/salário no
    funcionário, relação de unidade no morador) ainda são NOT NULL sem
    valor padrão na tabela real — o que quebra o INSERT feito pelo model
    novo, que não preenche mais esses campos. Tornamos elas opcionais.
    """
    _sep("6/6 — Tornando colunas legadas opcionais (NOT NULL -> NULL)")
    alteracoes = [
        ("funcionario", "cargo", "ALTER TABLE `funcionario` MODIFY COLUMN `cargo` VARCHAR(50) DEFAULT NULL"),
        ("funcionario", "salario_funcionario",
         "ALTER TABLE `funcionario` MODIFY COLUMN `salario_funcionario` DOUBLE DEFAULT NULL"),
        ("morador", "relacao_unidade",
         "ALTER TABLE `morador` MODIFY COLUMN `relacao_unidade` VARCHAR(50) DEFAULT NULL"),
    ]
    with conn.cursor() as cur:
        for tabela, coluna, sql in alteracoes:
            if not _tabela_existe(cur, tabela) or not _coluna_existe(cur, tabela, coluna):
                print(f"   ⏭  '{tabela}.{coluna}' não existe — pulando.")
                continue
            try:
                cur.execute(sql)
                conn.commit()
                print(f"   ✅ '{tabela}.{coluna}' agora aceita NULL.")
            except pymysql.MySQLError as e:
                print(f"   ⚠️  Não foi possível alterar '{tabela}.{coluna}': {e}")


def main():
    print("═" * 62)
    print("  Smart Condominium — Migration: pessoa x vínculo condomínio")
    print("═" * 62)

    print("\n🔌 Conectando ao banco...")
    conn = _get_conn()
    print(f"   ✅ Conectado em {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['db']}")

    try:
        criar_tabelas_associacao(conn)
        adicionar_documento_funcionario(conn)
        migrar_moradores(conn)
        migrar_funcionarios(conn)
        criar_indices_documento(conn)
        relaxar_colunas_legado(conn)
    finally:
        conn.close()

    print("\n" + "═" * 62)
    print("  ✅ Migration concluída!")
    print("  As colunas antigas foram mantidas (não usadas pelo código novo).")
    print("═" * 62 + "\n")


if __name__ == "__main__":
    main()
