"""
migration_usuario.py
====================
Adiciona a coluna `usuario` às tabelas `funcionario` e `morador`,
popula os registros existentes com usuario gerado automaticamente
(primeiro.ultimo) e trata colisões.

Uso:
    python migration_usuario.py

Dependência:
    pip install pymysql unidecode
    (unidecode remove acentos: João → joao)
"""

import re
import sys

import pymysql

try:
    from unidecode import unidecode
except ImportError:
    print("⚠️  Pacote 'unidecode' não encontrado. Instalando...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "unidecode"])
    from unidecode import unidecode

# ── Configuração do banco ──────────────────────────────────────
import os
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
    linha = "═" * 60
    print(f"\n{linha}")
    if titulo:
        print(f"  {titulo}")
        print(linha)


# ── Helpers de geração de usuário ─────────────────────────────

def _slugify(texto):
    """
    Converte texto para slug sem acentos, minúsculas, sem espaços.
    Exemplo: 'João Batista' → 'joao batista'
    """
    s = unidecode(texto or "").lower().strip()
    s = re.sub(r"[^a-z0-9\s]", "", s)   # remove tudo que não é letra/número/espaço
    return s


def _partes(nome):
    """Retorna lista de partes do nome em slug."""
    return [p for p in _slugify(nome).split() if p]


def _usuario_candidatos(nome):
    """
    Retorna lista de candidatos de usuário em ordem de prioridade:
      1. primeiro.ultimo
      2. primeiro.penultimo
      3. primeiro.segundo
      4. primeiro.ultimo + número sequencial (1, 2, 3...)
    """
    partes = _partes(nome)
    if not partes:
        return ["usuario"]

    primeiro = partes[0]

    candidatos = []
    if len(partes) >= 2:
        candidatos.append(f"{primeiro}.{partes[-1]}")          # primeiro.ultimo
    if len(partes) >= 3:
        candidatos.append(f"{primeiro}.{partes[-2]}")          # primeiro.penultimo
    if len(partes) >= 3:
        candidatos.append(f"{primeiro}.{partes[1]}")           # primeiro.segundo
    # Fallback com sufixo numérico
    base = f"{primeiro}.{partes[-1]}" if len(partes) >= 2 else primeiro
    for i in range(1, 100):
        candidatos.append(f"{base}{i}")

    return candidatos


def _escolher_usuario(nome, usados):
    """
    Retorna o primeiro candidato que não está em `usados`.
    `usados` é um set de strings.
    """
    for cand in _usuario_candidatos(nome):
        if cand not in usados:
            return cand
    # Fallback absoluto (nunca deve chegar aqui)
    import secrets
    return f"user_{secrets.token_hex(4)}"


# ── Lógica principal ───────────────────────────────────────────

def _tabela_existe(cur, tabela):
    cur.execute(
        "SELECT COUNT(*) AS n FROM information_schema.TABLES "
        "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s",
        (DB_CONFIG["db"], tabela)
    )
    return cur.fetchone()["n"] > 0


def _coluna_existe(cur, tabela, coluna):
    cur.execute(
        "SELECT COUNT(*) AS n FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s",
        (DB_CONFIG["db"], tabela, coluna)
    )
    return cur.fetchone()["n"] > 0


def _indice_existe(cur, tabela, nome_idx):
    cur.execute(
        "SELECT COUNT(*) AS n FROM information_schema.STATISTICS "
        "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND INDEX_NAME = %s",
        (DB_CONFIG["db"], tabela, nome_idx)
    )
    return cur.fetchone()["n"] > 0


def processar_tabela(conn, tabela):
    _sep(f"TABELA: {tabela}")
    with conn.cursor() as cur:

        # 1. Verificar se tabela existe
        if not _tabela_existe(cur, tabela):
            print(f"   ❌ Tabela '{tabela}' não encontrada — pulando.")
            return

        # 2. Adicionar coluna usuario
        if _coluna_existe(cur, tabela, "usuario"):
            print(f"   ⏭  Coluna '{tabela}.usuario' já existe.")
        else:
            cur.execute(f"""
                ALTER TABLE `{tabela}`
                ADD COLUMN `usuario` VARCHAR(80) DEFAULT NULL
                COMMENT 'Login: primeiro.ultimo (ex: joao.silva)'
                AFTER `nome`
            """)
            conn.commit()
            print(f"   ✅ Coluna '{tabela}.usuario' adicionada.")

        # 3. Adicionar índice UNIQUE
        idx_name = f"uq_{tabela}_usuario"
        if _indice_existe(cur, tabela, idx_name):
            print(f"   ⏭  Índice '{idx_name}' já existe.")
        else:
            cur.execute(f"""
                ALTER TABLE `{tabela}`
                ADD UNIQUE KEY `{idx_name}` (`usuario`)
            """)
            conn.commit()
            print(f"   ✅ Índice UNIQUE '{idx_name}' criado.")

        # 4. Buscar registros sem usuário
        cur.execute(f"SELECT id, nome FROM `{tabela}` WHERE usuario IS NULL OR usuario = ''")
        sem_usuario = cur.fetchall()

        if not sem_usuario:
            print(f"   ⏭  Nenhum registro sem usuário em '{tabela}'.")
        else:
            print(f"\n   🌱 Gerando usuários para {len(sem_usuario)} registro(s)...")

            # Carrega todos os usuários já em uso (funcionario + morador juntos)
            # Verifica se a coluna existe ANTES de consultar, pois pode estar
            # rodando a migration na ordem e a outra tabela ainda não tem a coluna.
            usados = set()
            for t in ("funcionario", "morador"):
                if _tabela_existe(cur, t) and _coluna_existe(cur, t, "usuario"):
                    cur.execute(f"SELECT usuario FROM `{t}` WHERE usuario IS NOT NULL AND usuario != ''")
                    for row in cur.fetchall():
                        usados.add(row["usuario"])

            atualizados = 0
            for reg in sem_usuario:
                usuario = _escolher_usuario(reg["nome"], usados)
                usados.add(usuario)

                cur.execute(
                    f"UPDATE `{tabela}` SET usuario = %s WHERE id = %s",
                    (usuario, reg["id"])
                )
                print(f"   ✅ #{reg['id']:>3} {reg['nome']:<30} → {usuario}")
                atualizados += 1

            conn.commit()
            print(f"\n   ✅ {atualizados} usuário(s) gerado(s) em '{tabela}'.")


def verificar_final(conn):
    _sep("VERIFICAÇÃO FINAL")
    with conn.cursor() as cur:
        for tabela in ("funcionario", "morador"):
            if not _tabela_existe(cur, tabela):
                continue
            cur.execute(f"SELECT id, nome, usuario FROM `{tabela}` ORDER BY id")
            rows = cur.fetchall()
            print(f"\n   📋 {tabela} ({len(rows)} registros):")
            print(f"   {'ID':<5} {'Nome':<30} {'Usuário'}")
            print(f"   {'-'*60}")
            for r in rows:
                print(f"   {r['id']:<5} {(r['nome'] or '—'):<30} {r['usuario'] or '—'}")


def main():
    print("\n" + "═" * 60)
    print("  Smart Condominium — Migration: coluna usuario")
    print("═" * 60)

    print("\n🔌 Conectando ao banco...")
    conn = _get_conn()
    print("   ✅ Conectado!")

    try:
        processar_tabela(conn, "funcionario")
        processar_tabela(conn, "morador")
        verificar_final(conn)
    finally:
        conn.close()

    print("\n" + "═" * 60)
    print("  ✅ Migration concluída com sucesso!")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    main()