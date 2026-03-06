import pandas as pd
import random
from pathlib import Path

PASTA_SAIDA = Path("./dados/original")
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

CPFS = ["52998224725", "98381654840", "12345678909", "11122233344", "55566677788", 
        "04335195095", "07370382257", "62597761525", "50221290605", "60608761290"]
NOMES = ['João Silva', 'Maria Santos', 'Carlos Oliveira', 'Ana Souza', 'Pedro Costa']
EMAILS = ['gmail.com', 'hotmail.com', 'yahoo.com.br']
TELEFONES = [f"119{random.randint(10000000, 99999999)}" for _ in range(80)]
CIDADES = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Brasília']

def gerar_cnpj():
    base = [random.randint(0, 9) for _ in range(12)]
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    s = sum(base[i] * pesos1[i] for i in range(12))
    dv1 = 0 if (s%11)<2 else 11-(s%11)
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    s = sum((base+[dv1])[i] * pesos2[i] for i in range(13))
    dv2 = 0 if (s%11)<2 else 11-(s%11)
    return ''.join(map(str, base + [dv1, dv2]))

CNPJS = [gerar_cnpj() for _ in range(15)]

def gerar_tabela_clientes(n):
    return pd.DataFrame({
        'id_cliente': range(1, n+1),
        'nome': [random.choice(NOMES) for _ in range(n)],
        'cpf': [random.choice(CPFS) for _ in range(n)],
        'email': [f"c{i}@{random.choice(EMAILS)}" for i in range(1, n+1)],
        'telefone': [random.choice(TELEFONES) for _ in range(n)]
    })

def gerar_tabela_cadastro(n):
    docs = [random.choice(CPFS) for _ in range(n)]
    return pd.DataFrame({
        'id': range(1, n+1),
        'nome': [random.choice(NOMES) for _ in range(n)],
        'ndoc_completo': docs,
        'cpf_cliente': docs,
        'cidade': [random.choice(CIDADES) for _ in range(n)]
    })

def gerar_tabela_fornecedores(n):
    return pd.DataFrame({
        'id_fornecedor': range(1, n+1),
        'razao_social': [f"Empresa {i} Ltda" for i in range(1, n+1)],
        'cnpj': [random.choice(CNPJS) for _ in range(n)],
        'email': [f"forn{i}@{random.choice(EMAILS)}" for i in range(1, n+1)],
        'telefone': [random.choice(TELEFONES) for _ in range(n)]
    })

def gerar_tabela_contratos(n):
    cnpjs = [random.choice(CNPJS) for _ in range(n)]
    return pd.DataFrame({
        'id_contrato': range(1, n+1),
        'descricao': [f"Contrato {i}" for i in range(1, n+1)],
        'cnpj_raiz': [c[:8] for c in cnpjs],
        'cnpj_complemento': [c[8:] for c in cnpjs],
        'valor': [random.randint(1000, 100000) for _ in range(n)]
    })

def gerar_tabela_parceiros(n):
    cnpjs = [random.choice(CNPJS) for _ in range(n)]
    return pd.DataFrame({
        'id_parceiro': range(1, n+1),
        'nome': [random.choice(NOMES) for _ in range(n)],
        'cnpj_raiz_unhash': [c[:8] for c in cnpjs],
        'cnpj_sufx': [c[8:12] for c in cnpjs],
        'cnpj_dig': [c[12:] for c in cnpjs],
        'ativo': [random.choice(['S', 'N']) for _ in range(n)]
    })

def gerar_tabela_mista(n):
    return pd.DataFrame({
        'id': range(1, n+1),
        'nome': [random.choice(NOMES) for _ in range(n)],
        'cpf': [random.choice(CPFS) for _ in range(n)],
        'cnpj_completo': [random.choice(CNPJS) for _ in range(n)],
        'email': [f"m{i}@{random.choice(EMAILS)}" for i in range(1, n+1)]
    })

def gerar_tabela_emails(n):
    return pd.DataFrame({
        'id': range(1, n+1),
        'email': [f"e{i}@{random.choice(EMAILS)}" for i in range(1, n+1)],
        'cidade': [random.choice(CIDADES) for _ in range(n)]
    })

def gerar_tabela_historica(n):
    base = random.sample(CPFS, 3)
    return pd.DataFrame({
        'ano': [2020 + (i % 5) for i in range(n)],
        'documento_ref': [base[i % 3] for i in range(n)],
        'valor': [1000 + i * 7 for i in range(n)]
    })

TABELAS = [
    ('clientes', gerar_tabela_clientes, 180),
    ('cadastro', gerar_tabela_cadastro, 120),
    ('fornecedores', gerar_tabela_fornecedores, 150),
    ('contratos', gerar_tabela_contratos, 120),
    ('parceiros', gerar_tabela_parceiros, 120),
    ('mista', gerar_tabela_mista, 140),
    ('emails', gerar_tabela_emails, 200),
    ('historica', gerar_tabela_historica, 240)
]

for nome, func, linhas in TABELAS:
    func(linhas).to_csv(PASTA_SAIDA / f"{nome}.csv", index=False)
    print(f"✅ {nome}.csv")