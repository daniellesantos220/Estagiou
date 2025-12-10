#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de teste.
- 20 estudantes
- 10 recrutadores
- 10 áreas de trabalho
- 2-5 vagas por recrutador
"""

import sqlite3
import random
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/Volumes/Externo/Ifes/PI/Estagiou')
from util.security import criar_hash_senha

# Lista de nomes brasileiros
NOMES_ESTUDANTES = [
    "Ana Silva", "Bruno Costa", "Carla Oliveira", "Daniel Santos", "Eduarda Lima",
    "Felipe Souza", "Gabriela Alves", "Henrique Rodrigues", "Isabela Ferreira", "João Martins",
    "Larissa Pereira", "Mateus Ribeiro", "Natália Cardoso", "Otávio Mendes", "Paula Barbosa",
    "Rafael Carvalho", "Sofia Araújo", "Thiago Gomes", "Vitória Dias", "Wesley Nascimento"
]

NOMES_RECRUTADORES = [
    "TechCorp RH", "Inovação Ltda", "StartUp Brasil", "Consultoria Plus", "Digital Solutions",
    "Recursos Humanos Pro", "Talentos SA", "Agência Empregos", "RH Master", "Carreira Já"
]

AREAS_TRABALHO = [
    ("Tecnologia da Informação", "Desenvolvimento de software, infraestrutura e suporte"),
    ("Administração", "Gestão empresarial, planejamento estratégico e processos"),
    ("Marketing", "Comunicação, branding, publicidade e mídias sociais"),
    ("Vendas", "Comercial, relacionamento com cliente e negócios"),
    ("Recursos Humanos", "Recrutamento, seleção e gestão de pessoas"),
    ("Financeiro", "Contabilidade, controladoria e análise financeira"),
    ("Engenharia", "Projetos, desenvolvimento e manutenção industrial"),
    ("Design", "Design gráfico, UX/UI e criação visual"),
    ("Educação", "Ensino, treinamento e desenvolvimento educacional"),
    ("Saúde", "Assistência médica, enfermagem e bem-estar")
]

TITULOS_VAGAS = {
    1: ["Desenvolvedor Full Stack", "Analista de Sistemas", "Suporte Técnico", "DevOps Engineer", "Cientista de Dados"],
    2: ["Assistente Administrativo", "Analista de Processos", "Coordenador de Projetos", "Auxiliar Administrativo"],
    3: ["Analista de Marketing", "Social Media", "Designer Gráfico", "Coordenador de Marketing"],
    4: ["Executivo de Vendas", "Gerente Comercial", "Representante de Vendas", "Coordenador de Vendas"],
    5: ["Analista de RH", "Recrutador", "Assistente de RH", "Business Partner"],
    6: ["Analista Financeiro", "Contador", "Auxiliar Contábil", "Controller"],
    7: ["Engenheiro de Produção", "Engenheiro Civil", "Engenheiro Mecânico", "Técnico em Engenharia"],
    8: ["Designer UX/UI", "Designer Gráfico", "Motion Designer", "Diretor de Arte"],
    9: ["Professor", "Instrutor", "Coordenador Pedagógico", "Tutor"],
    10: ["Enfermeiro", "Técnico de Enfermagem", "Médico", "Fisioterapeuta"]
}

MODALIDADES = ["Presencial", "Remoto", "Híbrido"]
CIDADES = ["Vitória", "Vila Velha", "Serra", "Cariacica", "Cachoeiro de Itapemirim", "Linhares", "São Mateus", "Colatina"]
UF = "ES"

def gerar_cpf():
    """Gera um CPF fictício válido"""
    def calcular_digito(digs):
        s = 0
        qtd = len(digs) + 1
        for i, d in enumerate(digs):
            s += int(d) * (qtd - i)
        res = 11 - (s % 11)
        return 0 if res > 9 else res

    cpf = [random.randint(0, 9) for _ in range(9)]
    cpf.append(calcular_digito(cpf))
    cpf.append(calcular_digito(cpf))
    return ''.join(map(str, cpf))

def gerar_cnpj():
    """Gera um CNPJ fictício válido"""
    def calcular_digito(digs, pesos):
        s = sum(int(d) * p for d, p in zip(digs, pesos))
        res = s % 11
        return 0 if res < 2 else 11 - res

    cnpj = [random.randint(0, 9) for _ in range(8)]
    cnpj.extend([0, 0, 0, 1])  # filial 0001

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    cnpj.append(calcular_digito(cnpj, pesos1))

    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    cnpj.append(calcular_digito(cnpj, pesos2))

    return ''.join(map(str, cnpj))

def gerar_telefone():
    """Gera um telefone fictício brasileiro"""
    ddd = random.choice(['27', '28'])  # DDDs do ES
    numero = f"9{random.randint(8000, 9999)}{random.randint(1000, 9999)}"
    return f"({ddd}) {numero[:5]}-{numero[5:]}"

def gerar_data_nascimento():
    """Gera data de nascimento entre 18 e 65 anos atrás"""
    hoje = datetime.now()
    anos_atras = random.randint(18, 65)
    return (hoje - timedelta(days=anos_atras*365 + random.randint(0, 365))).date()

def popular_banco():
    """Popula o banco de dados com os dados de teste"""
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()

    try:
        # Senha padrão para todos os usuários (hash de "senha123")
        senha_hash = criar_hash_senha("senha123")

        print("📝 Cadastrando 20 estudantes...")
        estudantes_ids = []
        for i, nome in enumerate(NOMES_ESTUDANTES, 1):
            email = f"estudante{i}@estagiou.com.br"
            cpf = gerar_cpf()
            telefone = gerar_telefone()
            data_nasc = gerar_data_nascimento()

            cursor.execute("""
                INSERT INTO usuario (nome, data_nascimento, email, numero_documento, telefone, senha, perfil, confirmado)
                VALUES (?, ?, ?, ?, ?, ?, 'estudante', 1)
            """, (nome, data_nasc, email, cpf, telefone, senha_hash))

            estudantes_ids.append(cursor.lastrowid)
            print(f"  ✓ {nome} - {email}")

        print(f"\n✅ {len(estudantes_ids)} estudantes cadastrados!\n")

        print("🏢 Cadastrando 10 recrutadores...")
        recrutadores_ids = []
        for i, nome in enumerate(NOMES_RECRUTADORES, 1):
            email = f"recrutador{i}@estagiou.com.br"
            cnpj = gerar_cnpj()
            telefone = gerar_telefone()

            cursor.execute("""
                INSERT INTO usuario (nome, email, numero_documento, telefone, senha, perfil, confirmado)
                VALUES (?, ?, ?, ?, ?, 'recrutador', 1)
            """, (nome, email, cnpj, telefone, senha_hash))

            recrutadores_ids.append(cursor.lastrowid)
            print(f"  ✓ {nome} - {email}")

        print(f"\n✅ {len(recrutadores_ids)} recrutadores cadastrados!\n")

        print("💼 Cadastrando 10 áreas de trabalho...")
        areas_ids = []
        for nome_area, descricao in AREAS_TRABALHO:
            cursor.execute("""
                INSERT INTO area (nome, descricao)
                VALUES (?, ?)
            """, (nome_area, descricao))

            areas_ids.append(cursor.lastrowid)
            print(f"  ✓ {nome_area}")

        print(f"\n✅ {len(areas_ids)} áreas cadastradas!\n")

        print("📋 Cadastrando vagas (2-5 por recrutador)...")
        total_vagas = 0
        for recrutador_id in recrutadores_ids:
            num_vagas = random.randint(2, 5)

            # Pegar o nome do recrutador
            cursor.execute("SELECT nome FROM usuario WHERE id = ?", (recrutador_id,))
            nome_recrutador = cursor.fetchone()[0]

            for _ in range(num_vagas):
                area_id = random.choice(areas_ids)
                titulo = random.choice(TITULOS_VAGAS[area_id])
                modalidade = random.choice(MODALIDADES)
                cidade = random.choice(CIDADES)
                num_vagas_disponivel = random.randint(1, 5)
                salario = round(random.uniform(1500, 8000), 2)
                carga_horaria = random.choice(["20h semanais", "30h semanais", "40h semanais", "44h semanais"])

                descricao = f"Estamos buscando profissionais para atuar como {titulo}. Ótima oportunidade de crescimento profissional."
                requisitos = "Ensino superior em andamento ou completo. Experiência na área será um diferencial."
                beneficios = "Vale transporte, Vale refeição, Plano de saúde, Convênio com academias"

                cursor.execute("""
                    INSERT INTO vaga (
                        id_area, id_recrutador, status_vaga, titulo, descricao,
                        numero_vagas, salario, requisitos, beneficios,
                        carga_horaria, modalidade, cidade, uf
                    ) VALUES (?, ?, 'aberta', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    area_id, recrutador_id, titulo, descricao,
                    num_vagas_disponivel, salario, requisitos, beneficios,
                    carga_horaria, modalidade, cidade, UF
                ))

                total_vagas += 1
                print(f"  ✓ {titulo} - {nome_recrutador} ({modalidade}, {cidade})")

        print(f"\n✅ {total_vagas} vagas cadastradas!\n")

        # Commit das alterações
        conn.commit()

        # Estatísticas finais
        print("=" * 60)
        print("📊 RESUMO DO CADASTRO")
        print("=" * 60)
        print(f"👨‍🎓 Estudantes: {len(estudantes_ids)}")
        print(f"🏢 Recrutadores: {len(recrutadores_ids)}")
        print(f"💼 Áreas: {len(areas_ids)}")
        print(f"📋 Vagas: {total_vagas}")
        print("=" * 60)
        print("\n💡 Credenciais de acesso:")
        print("   Email: estudante[1-20]@estagiou.com.br ou recrutador[1-10]@estagiou.com.br")
        print("   Senha: senha123")
        print("=" * 60)

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Erro ao popular banco de dados: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 INICIANDO POPULAÇÃO DO BANCO DE DADOS")
    print("=" * 60 + "\n")
    popular_banco()
    print("\n✅ Processo finalizado com sucesso!\n")
