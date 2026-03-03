import pandas as pd
import random
import numpy as np
from pathlib import Path


PASTA_SAIDA = Path("./dados/entrada")
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)


CPFS_VALIDOS = [
    "52998224725", "98381654840", "12345678909", 
    "11122233344", "55566677788", "04335195095",
    "07370382257", "62597761525", "50221290605",
    "60608761290", "63082785727"
]

TELEFONES = [f"119{random.randint(10**7, 10**8-1)}" for _ in range(50)]
EMAILS = [f"user{i}@{d}" for i in range(1,51) for d in ['gmail.com', 'hotmail.com', 'yahoo.com.br']]
NOMES = ['João Silva', 'Maria Santos', 'Carlos Oliveira', 'Ana Souza', 
         'Pedro Costa', 'Juliana Lima', 'Rafael Almeida', 'Camila Rodrigues']
CIDADES = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Brasília', 'Salvador', 'Porto Alegre']
EMPRESAS = ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Empresa E']
PRODUTOS = ['Celular', 'Notebook', 'Tablet', 'TV', 'Fone', 'Carregador']



def gerar_tabela_clientes(linhas=100):
    dados = {
        'id_cliente': range(1, linhas+1),
        'nome': [random.choice(NOMES) for _ in range(linhas)],
        'cpf': [random.choice(CPFS_VALIDOS) for _ in range(linhas)],
        'email': [f"cliente{i}@{random.choice(['gmail', 'hotmail', 'yahoo'])}.com" for i in range(1, linhas+1)],
        'telefone': [random.choice(TELEFONES) for _ in range(linhas)],
        'cidade': [random.choice(CIDADES) for _ in range(linhas)],
        'renda': [random.randint(2000, 15000) for _ in range(linhas)],
        'data_cadastro': [f"202{i%4+1}-{random.randint(1,12):02d}-{random.randint(1,28):02d}" for i in range(linhas)]
    }
    return pd.DataFrame(dados)

def gerar_tabela_clientes_sem_cpf(linhas=100):
    dados = {
        'id_cliente': range(1, linhas+1),
        'nome': [random.choice(NOMES) for _ in range(linhas)],
        'email': [f"cliente{i}@{random.choice(['gmail', 'hotmail', 'yahoo'])}.com" for i in range(1, linhas+1)],
        'cidade': [random.choice(CIDADES) for _ in range(linhas)],
        'data_cadastro': [f"202{i%4+1}-{random.randint(1,12):02d}-{random.randint(1,28):02d}" for i in range(linhas)]
    }
    return pd.DataFrame(dados)

def gerar_tabela_cadastro(linhas=100):
    cpfs = [random.choice(CPFS_VALIDOS) for _ in range(linhas)]
    dados = {
        'id_pessoa': range(1, linhas+1),
        'nome_completo': [random.choice(NOMES) for _ in range(linhas)],
        'documento': cpfs.copy(),  
        'cpf_cliente': cpfs.copy(), 
        'email': [f"pessoa{i}@{random.choice(['gmail', 'hotmail', 'yahoo'])}.com" for i in range(1, linhas+1)],
        'telefone': [random.choice(TELEFONES) for _ in range(linhas)],
        'endereco': [f"Rua {random.randint(1,100)}, {random.randint(1,1000)}" for _ in range(linhas)]
    }
    return pd.DataFrame(dados)

def gerar_tabela_emails(linhas=100):
    dados = {
        'id_email': range(1, linhas+1),
        'email': [f"contato{i}@{random.choice(['gmail', 'hotmail', 'yahoo'])}.com" for i in range(1, linhas+1)],
        'data_envio': [f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}" for _ in range(linhas)],
        'campanha': [f"Promoção {random.choice(['Verão', 'Inverno', 'Black Friday', 'Natal'])}" for _ in range(linhas)],
        'status': [random.choice(['Enviado', 'Aberto', 'Clique', 'Spam']) for _ in range(linhas)]
    }
    return pd.DataFrame(dados)

def gerar_tabela_telefones(linhas=100):
    dados = {
        'id_telefone': range(1, linhas+1),
        'telefone': [random.choice(TELEFONES) for _ in range(linhas)],
        'operadora': [random.choice(['Vivo', 'Claro', 'Tim', 'Oi']) for _ in range(linhas)],
        'ddd': [random.choice([11, 21, 31, 41, 51, 61, 71]) for _ in range(linhas)],
        'data_registro': [f"202{i%4+1}-{random.randint(1,12):02d}-{random.randint(1,28):02d}" for i in range(linhas)]
    }
    return pd.DataFrame(dados)

def gerar_tabela_historica(linhas=100):
    ""
    cpfs_base = random.sample(CPFS_VALIDOS, 5) 
    dados = []
    
    for i in range(linhas):
        cpf = cpfs_base[i % 5]  
        dados.append({
            'cpf': cpf,
            'ano': 2020 + (i % 4),
            'mes': random.randint(1, 12),
            'renda': 3000 + i * 100,
            'status': random.choice(['ATIVO', 'INATIVO']),
            'score': random.randint(300, 1000)
        })
    
    return pd.DataFrame(dados)

def gerar_tabela_com_nomes_diferentes(linhas=100):
    cpfs = [random.choice(CPFS_VALIDOS) for _ in range(linhas)]
    dados = {
        'id_registro': range(1, linhas+1),
        'nome': [random.choice(NOMES) for _ in range(linhas)],
        'num_documento': cpfs.copy(), 
        'doc_identificador': cpfs.copy(),  
        'cpf_titular': cpfs.copy(),  
        'telefone': [random.choice(TELEFONES) for _ in range(linhas)],
        'email': [f"reg{i}@{random.choice(['gmail', 'hotmail', 'yahoo'])}.com" for i in range(1, linhas+1)]
    }
    return pd.DataFrame(dados)

def gerar_tabela_mista(linhas=100):
    dados = {
        'id': range(1, linhas+1),
        'cpf': [random.choice(CPFS_VALIDOS) for _ in range(linhas)],
        'telefone': [random.choice(TELEFONES) for _ in range(linhas)],
        'email': [f"mix{i}@{random.choice(['gmail', 'hotmail', 'yahoo'])}.com" for i in range(1, linhas+1)],
        'nome': [random.choice(NOMES) for _ in range(linhas)],
        'idade': [random.randint(18, 80) for _ in range(linhas)],
        'salario': [random.randint(2000, 20000) for _ in range(linhas)]
    }
    return pd.DataFrame(dados)


TABELAS = [
    {"nome": "clientes", "funcao": gerar_tabela_clientes, "linhas": 200},
    {"nome": "clientes_sem_cpf", "funcao": gerar_tabela_clientes_sem_cpf, "linhas": 150},
    {"nome": "cadastro", "funcao": gerar_tabela_cadastro, "linhas": 100},
    {"nome": "emails", "funcao": gerar_tabela_emails, "linhas": 300},
    {"nome": "telefones", "funcao": gerar_tabela_telefones, "linhas": 250},
    {"nome": "historica", "funcao": gerar_tabela_historica, "linhas": 400},
    {"nome": "nomes_diferentes", "funcao": gerar_tabela_com_nomes_diferentes, "linhas": 120},
    {"nome": "mista", "funcao": gerar_tabela_mista, "linhas": 180},
]


def gerar_todas_tabelas():
    print(f"\n📂 Gerando tabelas em: {PASTA_SAIDA}")
    print("="*60)
    
    for config in TABELAS:
        print(f"📄 Gerando {config['nome']} com {config['linhas']} linhas...")
        df = config["funcao"](config["linhas"])
        arquivo = PASTA_SAIDA / f"{config['nome']}.csv"
        df.to_csv(arquivo, index=False)
        print(f"   ✅ Salvo: {arquivo}")
    
    print("\n" + "="*60)
    print(f"✅ Total de {len(TABELAS)} tabelas geradas!")

def gerar_tabela_especifica(nome, linhas=100):
    for config in TABELAS:
        if config["nome"] == nome:
            print(f"📄 Gerando {nome} com {linhas} linhas...")
            df = config["funcao"](linhas)
            arquivo = PASTA_SAIDA / f"{nome}.csv"
            df.to_csv(arquivo, index=False)
            print(f"✅ Salvo: {arquivo}")
            return
    
    print(f"❌ Tabela '{nome}' não encontrada!")



if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2:
        nome = sys.argv[1]
        linhas = int(sys.argv[2])
        gerar_tabela_especifica(nome, linhas)
    else:
        gerar_todas_tabelas()