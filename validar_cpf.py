import pandas as pd

AMOSTRA = 100
CONFIANCA = 0.7

def validar_cpf(v):
    if pd.isna(v): return False
    v = ''.join(filter(str.isdigit, str(v)))
    if len(v) != 11 or v == v[0]*11: return False
    s = sum(int(v[i])*(10-i) for i in range(9))
    if int(v[9]) != (0 if (r:=s%11)<2 else 11-r): return False
    s = sum(int(v[i])*(11-i) for i in range(10))
    return int(v[10]) == (0 if (r:=s%11)<2 else 11-r)

def colunas_cpf(df):
    a = df.head(AMOSTRA)
    return [c for c in df.columns 
            if len(v:=a[c].dropna()) > 0 
            and sum(validar_cpf(x) for x in v)/len(v) >= CONFIANCA]