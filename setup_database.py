"""
setup_database.py
=================
Script para criar todas as tabelas do Smart Condominium
e inserir os dados iniciais no banco de dados.

Uso:
    python setup_database.py

Dependência:
    pip install pymysql
"""

import pymysql
import sys

# ─── Configurações do banco ───────────────────────────────────────────────────
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

# ─── DDL — Criação das tabelas ────────────────────────────────────────────────
CREATE_TABLES = [
    # 1. condominio (sem dependências)
    """
    CREATE TABLE IF NOT EXISTS `condominio` (
        `id`                  INT(11)       NOT NULL AUTO_INCREMENT,
        `nome`                VARCHAR(100)  NOT NULL,
        `numero`              VARCHAR(10)   NOT NULL,
        `endereco`            VARCHAR(255)  NOT NULL,
        `cidade`              VARCHAR(100)  NOT NULL,
        `estado`              VARCHAR(50)   NOT NULL,
        `cep`                 VARCHAR(20)   NOT NULL,
        `telefone`            VARCHAR(20)   DEFAULT NULL,
        `celular`             VARCHAR(20)   NOT NULL,
        `email`               VARCHAR(100)  DEFAULT NULL,
        `sindico_nome`        VARCHAR(100)  DEFAULT NULL,
        `sindico_telefone`    VARCHAR(20)   DEFAULT NULL,
        `sindico_email`       VARCHAR(100)  DEFAULT NULL,
        `regras_regulamentos` TEXT          DEFAULT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """,

    # 2. unidade (depende de condominio)
    """
    CREATE TABLE IF NOT EXISTS `unidade` (
        `id`                      INT(11)       NOT NULL AUTO_INCREMENT,
        `condominio_id`           INT(11)       DEFAULT NULL,
        `numero_unidade`          VARCHAR(20)   NOT NULL,
        `proprietario_residente`  VARCHAR(100)  NOT NULL,
        `telefone_proprietario`   VARCHAR(20)   DEFAULT NULL,
        `email_proprietario`      VARCHAR(100)  DEFAULT NULL,
        `tipo_unidade`            VARCHAR(50)   NOT NULL,
        `status`                  VARCHAR(20)   NOT NULL,
        `area`                    DECIMAL(10,2) DEFAULT NULL,
        PRIMARY KEY (`id`),
        KEY `condominio_id` (`condominio_id`),
        CONSTRAINT `unidade_ibfk_1`
            FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """,

    # 3. morador (depende de unidade)
    """
    CREATE TABLE IF NOT EXISTS `morador` (
        `id`                   INT(11)      NOT NULL AUTO_INCREMENT,
        `unidade_id`           INT(11)      DEFAULT NULL,
        `nome`                 VARCHAR(100) NOT NULL,
        `data_nascimento`      DATE         DEFAULT NULL,
        `documento_identidade` VARCHAR(20)  DEFAULT NULL,
        `telefone`             VARCHAR(20)  DEFAULT NULL,
        `email`                VARCHAR(100) DEFAULT NULL,
        `relacao_unidade`      VARCHAR(50)  NOT NULL,
        `veiculo_placa`        VARCHAR(20)  DEFAULT NULL,
        `veiculo_modelo`       VARCHAR(50)  DEFAULT NULL,
        `veiculo_cor`          VARCHAR(50)  DEFAULT NULL,
        PRIMARY KEY (`id`),
        KEY `unidade_id` (`unidade_id`),
        CONSTRAINT `morador_ibfk_1`
            FOREIGN KEY (`unidade_id`) REFERENCES `unidade` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """,

    # 4. funcionario (depende de condominio)
    """
    CREATE TABLE IF NOT EXISTS `funcionario` (
        `id`                 INT(11)      NOT NULL AUTO_INCREMENT,
        `condominio_id`      INT(11)      DEFAULT NULL,
        `nome`               VARCHAR(100) NOT NULL,
        `cargo`              VARCHAR(50)  NOT NULL,
        `telefone`           VARCHAR(20)  DEFAULT NULL,
        `email`              VARCHAR(100) DEFAULT NULL,
        `horario_trabalho`   VARCHAR(100) DEFAULT NULL,
        `salario_funcionario` DOUBLE      NOT NULL,
        PRIMARY KEY (`id`),
        KEY `condominio_id` (`condominio_id`),
        CONSTRAINT `funcionario_ibfk_1`
            FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """,

    # 5. areacomum (depende de condominio)
    """
    CREATE TABLE IF NOT EXISTS `areacomum` (
        `id`            INT(11)      NOT NULL AUTO_INCREMENT,
        `condominio_id` INT(11)      DEFAULT NULL,
        `descricao`     VARCHAR(255) NOT NULL,
        `regras_uso`    TEXT         DEFAULT NULL,
        PRIMARY KEY (`id`),
        KEY `condominio_id` (`condominio_id`),
        CONSTRAINT `areacomum_ibfk_1`
            FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """,

    # 6. comunicacao (depende de condominio)
    """
    CREATE TABLE IF NOT EXISTS `comunicacao` (
        `id`            INT(11)      NOT NULL AUTO_INCREMENT,
        `condominio_id` INT(11)      DEFAULT NULL,
        `titulo`        VARCHAR(255) NOT NULL,
        `conteudo`      TEXT         NOT NULL,
        `data_envio`    DATE         NOT NULL,
        PRIMARY KEY (`id`),
        KEY `condominio_id` (`condominio_id`),
        CONSTRAINT `comunicacao_ibfk_1`
            FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """,

    # 7. documentolegal (depende de condominio)
    """
    CREATE TABLE IF NOT EXISTS `documentolegal` (
        `id`              INT(11)     NOT NULL AUTO_INCREMENT,
        `condominio_id`   INT(11)     DEFAULT NULL,
        `tipo_documento`  VARCHAR(50) NOT NULL,
        `descricao`       TEXT        DEFAULT NULL,
        PRIMARY KEY (`id`),
        KEY `condominio_id` (`condominio_id`),
        CONSTRAINT `documentolegal_ibfk_1`
            FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """,

    # 8. financeiro (depende de condominio)
    """
    CREATE TABLE IF NOT EXISTS `financeiro` (
        `id`                   INT(11)       NOT NULL AUTO_INCREMENT,
        `condominio_id`        INT(11)       DEFAULT NULL,
        `tipo_transacao`       VARCHAR(20)   NOT NULL,
        `descricao_transacao`  VARCHAR(255)  NOT NULL,
        `valor`                DECIMAL(10,2) NOT NULL,
        `data_transacao`       DATE          NOT NULL,
        PRIMARY KEY (`id`),
        KEY `condominio_id` (`condominio_id`),
        CONSTRAINT `financeiro_ibfk_1`
            FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """,

    # 9. manutencaoservicos (depende de condominio)
    """
    CREATE TABLE IF NOT EXISTS `manutencaoservicos` (
        `id`                 INT(11)       NOT NULL AUTO_INCREMENT,
        `condominio_id`      INT(11)       DEFAULT NULL,
        `descricao_servico`  TEXT          NOT NULL,
        `data_servico`       DATE          NOT NULL,
        `custo`              DECIMAL(10,2) DEFAULT NULL,
        `prestador_servico`  VARCHAR(100)  DEFAULT NULL,
        PRIMARY KEY (`id`),
        KEY `condominio_id` (`condominio_id`),
        CONSTRAINT `manutencaoservicos_ibfk_1`
            FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """,

    # 10. seguranca (depende de condominio)
    """
    CREATE TABLE IF NOT EXISTS `seguranca` (
        `id`              INT(11)     NOT NULL AUTO_INCREMENT,
        `condominio_id`   INT(11)     DEFAULT NULL,
        `tipo_registro`   VARCHAR(50) NOT NULL,
        `descricao`       TEXT        NOT NULL,
        `data_registro`   DATE        NOT NULL,
        PRIMARY KEY (`id`),
        KEY `condominio_id` (`condominio_id`),
        CONSTRAINT `seguranca_ibfk_1`
            FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """,
]

# ─── DML — Dados iniciais ─────────────────────────────────────────────────────
SEED_DATA = [
    # condominio
    (
        "INSERT IGNORE INTO `condominio` "
        "(`id`,`nome`,`numero`,`endereco`,`cidade`,`estado`,`cep`,`telefone`,`celular`,"
        "`email`,`sindico_nome`,`sindico_telefone`,`sindico_email`,`regras_regulamentos`) VALUES "
        "(1,'Residencial Primavera','','Rua das Flores, 100','São Paulo','SP','01234-567',"
        "'(11) 1234-5678','(11) 9876-5432','contato@residencialprimavera.com','Carlos Silva',"
        "'(11) 7654-3210','carlos.silva@email.com','Regras e regulamentos do condomínio Residencial Primavera...'),"
        "(2,'Parque das Flores','','Av. dos Girassóis, 200','Rio de Janeiro','RJ','20000-123',"
        "'(21) 5555-5555','(21) 9876-5432','contato@parquedasflores.com','Ana Santos',"
        "'(21) 8765-4321','ana.santos@email.com','Regras e regulamentos do condomínio Parque das Flores...'),"
        "(3,'Vista Bela','','Rua das Palmeiras, 300','Belo Horizonte','MG','30000-456',"
        "'(31) 3333-3333','(31) 8765-4321','contato@vistabela.com','João Oliveira',"
        "'(31) 7654-3210','joao.oliveira@email.com','Regras e regulamentos do condomínio Vista Bela...'),"
        "(4,'Sol Nascente','','Av. do Sol, 400','Brasília','DF','70000-789',"
        "'(61) 7777-7777','(61) 9876-5432','contato@solascente.com','Maria Silva',"
        "'(61) 8765-4321','maria.silva@email.com','Regras e regulamentos do condomínio Sol Nascente...'),"
        "(5,'Jardim das Flores','','Alameda das Tulipas, 500','Curitiba','PR','80000-901',"
        "'(41) 8888-8888','(41) 9876-5432','contato@jardimdasflores.com','Pedro Oliveira',"
        "'(41) 8765-4321','pedro.oliveira@email.com','Regras e regulamentos do condomínio Jardim das Flores...')"
    ),

    # unidade
    (
        "INSERT IGNORE INTO `unidade` "
        "(`id`,`condominio_id`,`numero_unidade`,`proprietario_residente`,`telefone_proprietario`,"
        "`email_proprietario`,`tipo_unidade`,`status`,`area`) VALUES "
        "(1,1,'101','Carlos Silva','(11) 1234-5678','carlos.silva@email.com','Apartamento','Ocupada',100.00),"
        "(2,1,'102','Mariana Santos','(11) 2345-6789','mariana.santos@email.com','Apartamento','Disponível',90.00),"
        "(3,1,'201','João Oliveira','(11) 3456-7890','joao.oliveira@email.com','Cobertura','Alugado',150.00),"
        "(4,1,'202','Ana Costa','(11) 4567-8901','ana.costa@email.com','Apartamento','Disponível',95.00),"
        "(5,1,'301','Paulo Souza','(11) 5678-9012','paulo.souza@email.com','Apartamento','Ocupada',110.00),"
        "(6,2,'A1','Pedro Oliveira','(21) 5555-5555','pedro.oliveira@email.com','Casa','Ocupada',200.00),"
        "(7,2,'A2','Luciana Costa','(21) 6666-6666','luciana.costa@email.com','Apartamento','Disponível',85.00),"
        "(8,2,'B1','Ana Oliveira','(21) 7777-7777','ana.oliveira@email.com','Cobertura','Ocupada',160.00),"
        "(9,2,'B2','Fernando Silva','(21) 8888-8888','fernando.silva@email.com','Apartamento','Disponível',100.00),"
        "(10,2,'C1','Marta Santos','(21) 9999-9999','marta.santos@email.com','Apartamento','Ocupada',120.00),"
        "(11,3,'101','Carla Oliveira','(31) 1111-1111','carla.oliveira@email.com','Apartamento','Ocupada',95.00),"
        "(12,3,'102','Renato Silva','(31) 2222-2222','renato.silva@email.com','Cobertura','Disponível',140.00),"
        "(13,3,'201','Mariana Costa','(31) 3333-3333','mariana.costa@email.com','Apartamento','Alugado',105.00),"
        "(14,3,'202','Joana Santos','(31) 4444-4444','joana.santos@email.com','Apartamento','Disponível',100.00),"
        "(15,3,'301','Luiz Oliveira','(31) 5555-5555','luiz.oliveira@email.com','Casa','Ocupada',180.00),"
        "(16,4,'101','Ricardo Santos','(61) 1111-1111','ricardo.santos@email.com','Apartamento','Disponível',90.00),"
        "(17,4,'102','Carolina Oliveira','(61) 2222-2222','carolina.oliveira@email.com','Apartamento','Ocupada',100.00),"
        "(18,4,'201','Roberto Silva','(61) 3333-3333','roberto.silva@email.com','Casa','Alugado',150.00),"
        "(19,4,'202','Fernanda Costa','(61) 4444-4444','fernanda.costa@email.com','Apartamento','Ocupada',110.00),"
        "(20,4,'301','Paula Santos','(61) 5555-5555','paula.santos@email.com','Cobertura','Disponível',160.00),"
        "(21,5,'101','Guilherme Oliveira','(41) 1111-1111','guilherme.oliveira@email.com','Apartamento','Ocupada',100.00),"
        "(22,5,'102','Helena Silva','(41) 2222-2222','helena.silva@email.com','Cobertura','Alugado',150.00),"
        "(23,5,'201','Luis Costa','(41) 3333-3333','luis.costa@email.com','Casa','Alugado',180.00),"
        "(24,5,'202','Alice Santos','(41) 4444-4444','alice.santos@email.com','Apartamento','Disponível',95.00),"
        "(25,5,'301','Júlia Oliveira','(41) 5555-5555','julia.oliveira@email.com','Apartamento','Ocupada',110.00)"
    ),

    # funcionario
    (
        "INSERT IGNORE INTO `funcionario` "
        "(`id`,`condominio_id`,`nome`,`cargo`,`telefone`,`email`,`horario_trabalho`,`salario_funcionario`) VALUES "
        "(1,1,'Maria Santos','sindico','(11) 1111-1111','maria.santos@residencialprimavera.com','Segunda a sexta, 08:00 - 17:00',2500),"
        "(2,5,'José Silva','sindico','(11) 2222-2222','jose.silva@residencialprimavera.com','Segunda a sexta, 08:00 - 17:00',3000),"
        "(3,2,'Ana Oliveira','sindico','(21) 3333-3333','ana.oliveira@parquedasflores.com','Segunda a sexta, 07:00 - 16:00',2400),"
        "(4,3,'Paulo Souza','sindico','(31) 4444-4444','paulo.souza@vistabela.com','Segunda a sexta, 09:00 - 18:00',2800),"
        "(5,4,'Luciana Costa','sindico','(61) 5555-5555','luciana.costa@solascente.com','Segunda a sexta, 08:30 - 17:30',2600)"
    ),

    # morador
    (
        "INSERT IGNORE INTO `morador` "
        "(`id`,`unidade_id`,`nome`,`data_nascimento`,`documento_identidade`,`telefone`,`email`,"
        "`relacao_unidade`,`veiculo_placa`,`veiculo_modelo`,`veiculo_cor`) VALUES "
        "(1,1,'Ana Oliveira','1985-03-15','123456789','(11) 9999-8888','ana.oliveira@email.com','Proprietário','ABC-1234','Toyota Corolla','Prata'),"
        "(2,1,'Pedro Oliveira','1978-07-22','987654321','(11) 8888-7777','pedro.oliveira@email.com','Inquilino','XYZ-9876','Honda Civic','Preto'),"
        "(3,2,'Lucas Santos','1990-10-05','456789123','(11) 7777-6666','lucas.santos@email.com','Proprietário','DEF-5678','Volkswagen Golf','Azul'),"
        "(4,3,'Marina Costa','1982-05-20','654321987','(11) 6666-5555','marina.costa@email.com','Proprietário','GHI-3456','Ford Fiesta','Vermelho'),"
        "(5,3,'Fernanda Silva','1995-12-12','789123456','(11) 5555-4444','fernanda.silva@email.com','Inquilino','JKL-9012','Chevrolet Onix','Branco'),"
        "(6,6,'Gustavo Oliveira','1987-08-18','987654321','(21) 9999-8888','gustavo.oliveira@email.com','Proprietário','MNO-2345','Fiat Uno','Vermelho'),"
        "(7,6,'Amanda Santos','1993-04-25','456789123','(21) 8888-7777','amanda.santos@email.com','Inquilino','PQR-6789','Renault Sandero','Prata'),"
        "(8,7,'Juliana Costa','1975-11-30','654321987','(21) 7777-6666','juliana.costa@email.com','Proprietário','STU-7890','Chevrolet Prisma','Preto'),"
        "(9,8,'Rafael Silva','1988-06-08','789123456','(21) 6666-5555','rafael.silva@email.com','Proprietário','VWX-1234','Hyundai HB20','Azul'),"
        "(10,8,'Camila Oliveira','1980-03-10','321987654','(21) 5555-4444','camila.oliveira@email.com','Inquilino','YZA-5678','Volkswagen Polo','Branco'),"
        "(11,9,'Fábio Santos','1984-09-03','987654321','(31) 9999-8888','fabio.santos@email.com','Proprietário','BCD-3456','Toyota Etios','Prata'),"
        "(12,9,'Laura Costa','1979-02-28','456789123','(31) 8888-7777','laura.costa@email.com','Proprietário','EFG-6789','Fiat Palio','Vermelho'),"
        "(13,10,'Gabriel Silva','1992-07-14','654321987','(31) 7777-6666','gabriel.silva@email.com','Inquilino','HIJ-7890','Renault Duster','Preto'),"
        "(14,11,'Carolina Oliveira','1986-12-22','789123456','(31) 6666-5555','carolina.oliveira@email.com','Proprietário','KLM-1234','Honda Fit','Azul'),"
        "(15,11,'Matheus Santos','1981-05-17','321987654','(31) 5555-4444','matheus.santos@email.com','Inquilino','NOP-5678','Chevrolet Spin','Branco'),"
        "(16,12,'Vanessa Costa','1989-11-11','987654321','(61) 9999-8888','vanessa.costa@email.com','Proprietário','PQR-3456','Fiat Toro','Prata'),"
        "(17,12,'Bruno Silva','1977-06-04','456789123','(61) 8888-7777','bruno.silva@email.com','Inquilino','STU-6789','Volkswagen Voyage','Vermelho'),"
        "(18,13,'Fernando Oliveira','1980-03-29','654321987','(61) 7777-6666','fernando.oliveira@email.com','Proprietário','VWX-7890','Chevrolet Tracker','Preto'),"
        "(19,14,'Aline Santos','1991-08-15','789123456','(61) 6666-5555','aline.santos@email.com','Proprietário','YZA-1234','Ford Ecosport','Azul'),"
        "(20,14,'Daniel Costa','1976-12-08','321987654','(61) 5555-4444','daniel.costa@email.com','Inquilino','BCD-5678','Toyota Hilux','Branco'),"
        "(21,15,'Isabela Oliveira','1994-04-20','987654321','(41) 9999-8888','isabela.oliveira@email.com','Proprietário','EFG-3456','Renault Kwid','Prata'),"
        "(22,15,'Gustavo Santos','1983-09-16','456789123','(41) 8888-7777','gustavo.santos@email.com','Inquilino','HIJ-6789','Fiat Siena','Vermelho'),"
        "(23,16,'Julia Silva','1988-02-09','654321987','(41) 7777-6666','julia.silva@email.com','Proprietário','KLM-7890','Chevrolet','Vermelho')"
    ),
]

# ─── Nomes amigáveis das tabelas para o log ───────────────────────────────────
TABLE_NAMES = [
    "condominio", "unidade", "morador", "funcionario",
    "areacomum", "comunicacao", "documentolegal",
    "financeiro", "manutencaoservicos", "seguranca",
]

SEED_NAMES = ["condominio (5 registros)", "unidade (25 registros)",
              "funcionario (5 registros)", "morador (23 registros)"]


def conectar():
    print("\n🔌 Conectando ao banco de dados...")
    try:
        conn = pymysql.connect(**DB_CONFIG)
        print("   ✅ Conexão estabelecida com sucesso!")
        return conn
    except pymysql.MySQLError as e:
        print(f"   ❌ Falha na conexão: {e}")
        sys.exit(1)


def criar_tabelas(conn):
    print("\n📦 Criando tabelas...")
    with conn.cursor() as cursor:
        # Desativa FK checks temporariamente para criação limpa
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        for i, ddl in enumerate(CREATE_TABLES):
            table = TABLE_NAMES[i]
            try:
                cursor.execute(ddl)
                print(f"   ✅ Tabela '{table}' — OK")
            except pymysql.MySQLError as e:
                print(f"   ❌ Erro na tabela '{table}': {e}")
                conn.rollback()
                sys.exit(1)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    conn.commit()
    print("   ✅ Todas as tabelas criadas!")


def inserir_dados(conn):
    print("\n🌱 Inserindo dados iniciais...")
    with conn.cursor() as cursor:
        for i, dml in enumerate(SEED_DATA):
            name = SEED_NAMES[i]
            try:
                cursor.execute(dml)
                print(f"   ✅ {name} — inserido(s)")
            except pymysql.MySQLError as e:
                print(f"   ⚠️  {name} — ignorado (já existente ou erro): {e}")
    conn.commit()
    print("   ✅ Dados iniciais inseridos!")


def verificar_tabelas(conn):
    print("\n🔍 Verificando tabelas criadas...")
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        tabelas = [row[0] for row in cursor.fetchall()]

    if tabelas:
        print(f"   📋 {len(tabelas)} tabela(s) encontrada(s) no banco '{DB_CONFIG['db']}':")
        for t in tabelas:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) FROM `{t}`;")
                total = cursor.fetchone()[0]
            print(f"      • {t:<25} {total} registro(s)")
    else:
        print("   ⚠️  Nenhuma tabela encontrada.")


def main():
    print("=" * 55)
    print("   Smart Condominium — Setup do Banco de Dados")
    print("=" * 55)

    conn = conectar()

    try:
        criar_tabelas(conn)
        inserir_dados(conn)
        verificar_tabelas(conn)
    finally:
        conn.close()

    print("\n" + "=" * 55)
    print("   ✅ Setup concluído com sucesso!")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()