"""
criar_admin.py
================
Cria (ou reativa) um usuário administrador inicial — um "funcionário"
com cargo "administrador", já vinculado a um condomínio (usa o primeiro
condomínio cadastrado; se não existir nenhum, cria um "Condomínio Padrão"
que você edita depois pelo painel).

Uso:
    python criar_admin.py
    python criar_admin.py --usuario admin --senha "Admin@123" --nome "Administrador" --email admin@seudominio.com

Se o usuário já existir, o script só atualiza a senha e garante que a
conta está ativa (não duplica nada) — pode rodar de novo com segurança.
"""
import argparse
import sys

from werkzeug.security import generate_password_hash

from condominio import app, db
from condominio.models.condominio_model import Condominio
from condominio.models.funcionario_model import Funcionario
from condominio.models.funcionario_condominio_model import FuncionarioCondominio


def main():
    parser = argparse.ArgumentParser(description="Cria o usuário administrador inicial.")
    parser.add_argument("--usuario", default="admin")
    parser.add_argument("--senha", default="Admin@123")
    parser.add_argument("--nome", default="Administrador")
    parser.add_argument("--email", default=None)
    parser.add_argument("--cargo", default="administrador", choices=["administrador", "sindico"])
    args = parser.parse_args()

    with app.app_context():
        existente = Funcionario.query.filter_by(usuario=args.usuario).first()

        if existente:
            existente.senha_hash = generate_password_hash(args.senha)
            existente.ativo = True
            db.session.commit()
            print(f"⏭  Usuário '{args.usuario}' já existia — senha redefinida e conta reativada.")
            func = existente
        else:
            func = Funcionario(nome=args.nome, usuario=args.usuario, email=args.email)
            func.senha_hash = generate_password_hash(args.senha)
            func.ativo = True
            db.session.add(func)
            db.session.commit()
            print(f"✅ Usuário '{args.usuario}' criado (id={func.id}).")

        # Garante vínculo com pelo menos um condomínio, senão o cargo não "existe" para o app
        tem_vinculo = FuncionarioCondominio.query.filter_by(funcionario_id=func.id, ativo=True).first()
        if not tem_vinculo:
            condominio = Condominio.query.order_by(Condominio.id.asc()).first()
            if not condominio:
                condominio = Condominio(
                    nome="Condomínio Padrão", endereco="A definir", cidade="A definir",
                    estado="--", cep="00000-000", celular="00000000000",
                )
                db.session.add(condominio)
                db.session.commit()
                print(f"✅ Criado '{condominio.nome}' (id={condominio.id}) — edite os dados reais depois pelo painel.")

            vinculo = FuncionarioCondominio(
                funcionario_id=func.id, condominio_id=condominio.id,
                cargo=args.cargo, salario_funcionario=0,
            )
            db.session.add(vinculo)
            db.session.commit()
            print(f"✅ Vínculo criado: '{args.usuario}' como '{args.cargo}' em '{condominio.nome}'.")
        else:
            print(f"⏭  Usuário já tinha vínculo ativo com condomínio — mantido como está.")

    print("\n" + "═" * 50)
    print(f"  Login:  {args.usuario}")
    print(f"  Senha:  {args.senha}")
    print("═" * 50)
    print("\n⚠️  Troque essa senha depois do primeiro login.")


if __name__ == "__main__":
    sys.exit(main())
