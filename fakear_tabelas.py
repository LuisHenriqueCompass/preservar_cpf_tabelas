import pandas as pd
import random
import sys
from pathlib import Path
from validar_cpf import colunas_cpf

RUAS = ['Rua Augusta', 'Av Paulista', 'Rua da Consolação', 'Av Brasil', 'Rua das Flores']
CIDADES = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Brasília']
ESTADOS = ['SP', 'RJ', 'MG', 'PR', 'DF']
EMAILS = ['gmail.com', 'hotmail.com', 'yahoo.com.br']
NOMES = ['João Silva', 'Maria Santos', 'Carlos Oliveira', 'Ana Souza', 'Pedro Costa']
TELEFONES = [f"119{random.randint(1000,9999)}{random.randint(1000,9999)}" for _ in range(100)]

def gerar_fake(df, cols_cpf):
    d = df.copy()
    
    for c in df.columns:
        if c in cols_cpf: continue
        
        cl = c.lower()
        if any(x in cl for x in ['rua', 'av', 'end']):
            d[c] = [f"{random.choice(RUAS)}, {random.randint(1,999)}" for _ in range(len(df))]
        elif 'cidade' in cl:
            d[c] = [random.choice(CIDADES) for _ in range(len(df))]
        elif 'estado' in cl or 'uf' in cl:
            d[c] = [random.choice(ESTADOS) for _ in range(len(df))]
        elif 'email' in cl:
            d[c] = [f"user{random.randint(1,9999)}@{random.choice(EMAILS)}" for _ in range(len(df))]
        elif any(x in cl for x in ['tel', 'fone']):
            d[c] = [random.choice(TELEFONES) for _ in range(len(df))]
        elif 'nome' in cl:
            d[c] = [random.choice(NOMES) for _ in range(len(df))]
        elif 'data' in cl:
            d[c] = [f"{random.randint(1,28):02d}/{random.randint(1,12):02d}/{random.randint(1980,2000)}" for _ in range(len(df))]
        elif df[c].dtype in ['int64','float64']:
            d[c] = [random.randint(1000, 9999) for _ in range(len(df))]
        else:
            d[c] = [f"{c}_{random.randint(1000,9999)}" for _ in range(len(df))]
    
    return d

def main():
    pasta = Path(sys.argv[1])
    
    saida = pasta / ".." / "fake"
    saida = saida.resolve()  
    saida.mkdir(parents=True, exist_ok=True) 
    
    print(f"📂 Entrada: {pasta}")
    print(f"📂 Saída: {saida}")
    
    for arq in pasta.glob("*.csv"):
        print(f"\n📄 Processando: {arq.name}")
        df = pd.read_csv(arq, dtype=str)
        cpf_cols = colunas_cpf(df)
        
        if cpf_cols:
            gerar_fake(df, cpf_cols).to_csv(saida / f"{arq.stem}_fake.csv", index=False)
            print(f"✅ Preservou: {cpf_cols}")
        else:
            print(f"⏭️ Sem CPF, ignorado")

if __name__ == "__main__":
    main()