# Smart Condominium — API REST

API JSON + JWT criada em cima do backend Flask existente, para ser consumida
pelo **app mobile (React Native / Expo)** e, opcionalmente, por um futuro
front-end SPA. O site atual continua funcionando exatamente como antes
(as rotas HTML/Jinja não foram alteradas em nada, exceto a remoção das
credenciais hardcoded).

## 0. Antes de tudo: rotacione a senha do banco

A senha do MySQL estava commitada em texto puro no repositório público
(`views.py`, `invite_views.py`, `setup_database.py`, scripts de migração).
Isso significa que qualquer pessoa que já viu o repositório (ou o histórico
do git) tem essa senha. Antes de colocar isso em produção:

1. Troque a senha do usuário `mysql` no MySQL do EasyPanel.
2. Nunca mais commite esse valor — ele agora vem de variável de ambiente.

## 1. Configuração

```bash
cp .env.example .env
# edite o .env com os valores reais (host, senha nova, chaves secretas)
```

Gerar chaves aleatórias para `SECRET_KEY` e `JWT_SECRET_KEY`:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

No **EasyPanel**, cadastre as mesmas variáveis em Environment (não suba o `.env`).

Instalar dependências novas:
```bash
pip install -r requirements.txt
```

## 2. Rodando localmente

```bash
python run.py
```

A API sobe junto com o site, em `/api/v1/*`. Teste:
```bash
curl http://localhost:5000/api/v1/saude
```

## 3. Autenticação

Login único para funcionário ou morador (usuário ou e-mail):

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"credencial": "maria.sindica", "senha": "sua-senha"}'
```

Resposta: `access_token` (8h) + `refresh_token` (30 dias). Envie o access
token em todas as chamadas protegidas:
```
Authorization: Bearer <access_token>
```

Renovar o access token:
```bash
curl -X POST http://localhost:5000/api/v1/auth/refresh \
  -H "Authorization: Bearer <refresh_token>"
```

## 4. Endpoints

Todos sob o prefixo `/api/v1`. Respostas sempre no formato:
```json
{ "sucesso": true, "dados": ... }
{ "sucesso": false, "erro": "mensagem" }
```

| Recurso | Rotas | Quem pode escrever |
|---|---|---|
| `/auth` | `POST /login`, `POST /refresh`, `GET /me`, `GET /contexto` | — |
| `/moradores` | `GET`, `GET /:id`, `POST`, `POST /vincular`, `PUT/PATCH /:id`, `DELETE /:id`, `DELETE /:id/desvincular/:vinculo_id` | síndico, administrador |
| `/funcionarios` | idem (`POST /vincular` liga a um novo condomínio) | síndico, administrador |
| `/pessoas` | `GET /buscar-documento/:cpf?tipo=morador\|funcionario` (dedup) | síndico, administrador |
| `/escalas` | idem (`?funcionario_id=`) | síndico, administrador |
| `/convites` | `POST /reenviar/:tipo/:id`, `GET /validar/:token`, `POST /aceitar` | síndico/administrador (reenviar) |
| `/condominios` | CRUD completo | síndico, administrador |
| `/unidades` | CRUD completo | síndico, administrador |
| `/areas-comuns` | CRUD completo | síndico, administrador |
| `/comunicados` | CRUD completo | síndico, administrador, porteiro |
| `/documentos` | CRUD completo | síndico, administrador |
| `/financeiro` | CRUD completo | síndico, administrador |
| `/manutencoes` | CRUD completo | síndico, administrador |
| `/seguranca` | CRUD completo | síndico, administrador, porteiro, segurança |
| `/saude` | `GET` (healthcheck, público) | — |

Listagens (`GET` de coleção) aceitam paginação: `?pagina=1&por_pagina=20`.

## 5. Onboarding de morador/funcionário (fluxo de convite)

1. Síndico cria o cadastro: `POST /moradores` ou `POST /funcionarios`
   (nasce com `ativo=false`, sem senha).
2. Síndico dispara o convite: `POST /convites/reenviar/morador/:id`
   → devolve um `token`. **Hoje o e-mail não é enviado de verdade** (só o
   token volta na resposta, para você plugar um provedor de e-mail depois —
   SendGrid, SES, etc. O código antigo só imprimia o link no console).
3. App/site chama `GET /convites/validar/:token` para checar validade.
4. Usuário define a senha: `POST /convites/aceitar { token, senha }`
   → conta fica `ativo=true` e pronta para login.

## 6. Modelagem pessoa × vínculo (multi-condomínio)

Uma pessoa (morador ou funcionário) agora é uma **identidade única** —
login, CPF, dados pessoais. Onde ela mora/trabalha é um **vínculo**
separado, então a mesma pessoa pode ter apartamentos ou atuar como
síndico em vários condomínios sem duplicar cadastro:

- `morador` (pessoa) 1—N `morador_unidade` (vínculo com uma unidade)
- `funcionario` (pessoa) 1—N `funcionario_condominio` (vínculo com um condomínio + cargo)

**Login (`POST /auth/login`)** devolve, além dos tokens, um objeto
`contexto` já pronto para o app renderizar a tela certa:
- morador: `condominios_morador` — lista de condomínios, cada um com as
  unidades daquela pessoa naquele condomínio (dados completos do apê).
- síndico/funcionário: `condominios_funcionario` — lista de condomínios
  onde atua, com o cargo em cada um, e `cargo_efetivo` (o cargo de maior
  privilégio entre todos os vínculos, usado para permissões).
- se a mesma pessoa for funcionário E morador (mesmo e-mail), o contexto
  traz os dois blocos.

Recarregar o contexto sem logar de novo: `GET /auth/contexto` (com o token).

**Deduplicação por CPF** — antes de cadastrar alguém novo, busque:
```
GET /pessoas/buscar-documento/<cpf>?tipo=morador   (ou tipo=funcionario)
```
Se a pessoa já existe, devolve só os dados pessoais (nunca apartamento/
cargo). Aí você usa:
```
POST /moradores/vincular      { documento_identidade, unidade_id, relacao_unidade, ... }
POST /funcionarios/vincular   { documento_identidade, condominio_id, cargo, ... }
```
para associar a pessoa existente ao novo condomínio/unidade, sem
recriar o cadastro pessoal. `POST /moradores` e `POST /funcionarios`
(criar pessoa nova) bloqueiam com `409` se o CPF já existir, sugerindo
usar `/vincular`.

### Migration necessária

Depois de configurar o `.env` com o banco novo, rode uma vez:
```bash
python migrate_pessoa_condominio.py
```
Ela cria `morador_unidade` e `funcionario_condominio`, adiciona CPF ao
funcionário, e copia os vínculos que já existem hoje (é idempotente —
pode rodar de novo sem duplicar nada). **Eu não consegui rodar essa
migration contra o seu banco real a partir daqui** (meu ambiente de
execução não tem rota de rede até `easypanel.pontocomdesconto.com.br`)
— toda a lógica foi validada com um banco de teste com a mesma
estrutura, mas rode a migration num ambiente de homologação antes de ir
pra produção, e faça backup antes.

⚠️ Isso também significa que as páginas HTML do site (login/perfil, que
usam SQL cru em `views.py`) continuam olhando só para as colunas antigas
(`morador.unidade_id`) — ou seja, o site segue mostrando **um único
apartamento** por morador até você migrar essas telas para consumir a
nova API. O app mobile, por outro lado, já nasce usando o modelo novo
(multi-condomínio) desde o primeiro endpoint.

## 7. O que muda no código existente

- `condominio/db_raw.py`: helper único de conexão MySQL "crua", lendo do
  `app.config` — elimina as 3 cópias de credenciais hardcoded.
- `config.py`: 100% via variáveis de ambiente (com validação — a app não
  sobe se faltar alguma).
- Novos models (`funcionario_model.py`, `unidade_model.py`,
  `escala_model.py`, `areacomum_model.py`, `comunicacao_model.py`,
  `documentolegal_model.py`, `financeiro_model.py`, `manutencao_model.py`,
  `seguranca_model.py`) — refletem o schema real do banco (o que antes só
  existia como SQL cru espalhado pelas views).
- `condominio/api/`: pacote novo com toda a API. Nada nas rotas HTML
  existentes foi removido ou quebrado.

## 8. Próximos passos sugeridos

- Rodar `migrate_pessoa_condominio.py` em homologação, validar, só então em produção.
- Enviar e-mail de verdade no convite (Flask-Mail + SMTP/SES).
- Adicionar rate limiting no `/auth/login` (Flask-Limiter) contra força bruta.
- Trocar o fallback de síndicos com senha fixa (`"sindico123"`) em
  `views.py` por contas reais no banco, e remover esse bloco.
- Migrar as telas SSR (login/perfil) para consumir a nova API/contexto,
  ou aposentá-las quando o app mobile cobrir o mesmo uso.
- Gerar coleção Postman/Insomnia ou OpenAPI a partir destas rotas.
- Começar o app mobile (React Native / Expo): tela inicial = login;
  depois do login, decide a Home a partir do `contexto` (se `tipo` é
  morador com 1 condomínio → vai direto pra Home dele; se tem mais de
  um → tela de seleção de condomínio; se é síndico/funcionário →
  dashboard com os condomínios onde atua).
