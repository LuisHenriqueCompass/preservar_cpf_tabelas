import pandas as pd
import random
import sys
from pathlib import Path
from validar_documentos import detectar_grupos_sensveis

NOMES = ['João Silva', 'Maria Santos', 'Carlos Oliveira', 'Ana Souza', 'Pedro Costa']
EMAILS = ['gmail.com', 'hotmail.com', 'yahoo.com.br']

def gerar_fake(df, cols_preservar):
    d = df.copy()
    for c in df.columns:
        if c in cols_preservar: continue
        cl = c.lower()
        if 'email' in cl:
            d[c] = [f"user{random.randint(1,9999)}@{random.choice(EMAILS)}" for _ in range(len(df))]
        elif 'nome' in cl or 'razao' in cl:
            d[c] = [random.choice(NOMES) if 'nome' in cl else f"Empresa {random.randint(1,9999)}" for _ in range(len(df))]
        elif df[c].dtype in ['int64','float64']:
            d[c] = [random.randint(1000, 9999) for _ in range(len(df))]
        else:
            d[c] = [f"{c}_{random.randint(1000,9999)}" for _ in range(len(df))]
    return d

def main():
    if len(sys.argv) < 2:
        print("Uso: python fakear_tabelas.py <pasta_entrada>")
        sys.exit(1)
    
    pasta = Path(sys.argv[1])
    saida = (pasta / ".." / "fake").resolve()
    saida.mkdir(parents=True, exist_ok=True)
    
    print(f"Entrada: {pasta}")
    print(f"Saída: {saida}\n")
    
    for arq in sorted(pasta.glob("*.csv")):
        print(f"{'='*60}\n{arq.name}\n{'='*60}")
        
        df = pd.read_csv(arq, dtype=str)
        analise = detectar_grupos_sensveis(df)
        
        cols_cpf = analise['completos']['cpf']
        cols_cnpj = analise['completos']['cnpj']
        
        if cols_cpf: print(f"CPF: {cols_cpf}")
        if cols_cnpj: print(f"CNPJ: {cols_cnpj}")
        
        if analise['grupos']:
            print(f"\nGrupos detectados:")
            for i, sug in enumerate(analise['sugestoes'], 1):
                print(f"  {i}. {sug['ordem']} -> {sug['tipo'].upper()} ({sug['taxa']*100:.0f}%)")
        
        cols_preservar = set(cols_cpf + cols_cnpj)
        for grupo in analise['grupos']:
            cols_preservar.update(grupo)
        
        if cols_preservar:
            gerar_fake(df, cols_preservar).to_csv(saida / f"{arq.stem}_fake.csv", index=False)
            print(f"\nSalvo: {arq.stem}_fake.csv\n")
        else:
            print(f"Sem documentos - arquivo copiado\n")
            df.to_csv(saida / f"{arq.stem}_fake.csv", index=False)

if __name__ == "__main__":
    main()