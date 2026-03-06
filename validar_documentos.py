import pandas as pd
from itertools import combinations

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

def validar_cnpj(v):
    if pd.isna(v): return False
    v = ''.join(filter(str.isdigit, str(v)))
    if len(v) != 14 or v == v[0]*14: return False
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    s = sum(int(v[i]) * pesos1[i] for i in range(12))
    if int(v[12]) != (0 if (r:=s%11)<2 else 11-r): return False
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    s = sum(int(v[i]) * pesos2[i] for i in range(13))
    return int(v[13]) == (0 if (r:=s%11)<2 else 11-r)

def colunas_cpf(df):
    a = df.head(AMOSTRA)
    return [c for c in df.columns if len(v:=a[c].dropna()) > 0 and sum(validar_cpf(x) for x in v)/len(v) >= CONFIANCA]

def colunas_cnpj(df):
    a = df.head(AMOSTRA)
    return [c for c in df.columns if len(v:=a[c].dropna()) > 0 and sum(validar_cnpj(x) for x in v)/len(v) >= CONFIANCA]

def detectar_grupos_sensveis(df):
    resultado = {'completos': {'cpf': colunas_cpf(df), 'cnpj': colunas_cnpj(df)}, 'grupos': [], 'sugestoes': []}
    
    a = df.head(AMOSTRA)
    candidatos = [c for c in df.columns if len(v:=a[c].dropna()) > 0 and 
                  sum(1 <= len(''.join(filter(str.isdigit, str(x)))) <= 14 for x in v)/len(v) >= CONFIANCA]
    
    if len(candidatos) < 2: return resultado
    
    for r in range(2, min(len(candidatos) + 1, 4)):
        for comb in combinations(candidatos, r):
            combinada = a[comb[0]].astype(str).str.cat([a[c].astype(str) for c in comb[1:]])
            taxa_cpf = sum(validar_cpf(x) for x in combinada.dropna()) / len(combinada)
            taxa_cnpj = sum(validar_cnpj(x) for x in combinada.dropna()) / len(combinada)
            
            if taxa_cpf >= CONFIANCA:
                resultado['grupos'].append(comb)
                resultado['sugestoes'].append({'taxa': taxa_cpf, 'tipo': 'cpf', 'ordem': list(comb)})
            elif taxa_cnpj >= CONFIANCA:
                resultado['grupos'].append(comb)
                resultado['sugestoes'].append({'taxa': taxa_cnpj, 'tipo': 'cnpj', 'ordem': list(comb)})
    
    return resultado