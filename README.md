# Gerador de Dados Fake com Preservação de Documentos

Sistema que gera versões fake de arquivos CSV preservando **CPF e CNPJ** (completos ou divididos).

## 🚀 Uso

```bash
# 1. Gerar dados de teste
python gerar_tabelas.py

# 2. Fakear dados (preservando documentos)
python fakear_tabelas.py dados/original/
```

## 💡 Como funciona

- **Detecta automaticamente** CPF/CNPJ por validação algorítmica (não pelo nome da coluna)
- **Preserva documentos** completos ou divididos em múltiplas colunas
- **Fakeia todo o resto** (nomes, emails, valores, etc)

## 🧠 Funcionamento Interno (Detalhado)

Esta seção explica exatamente como o sistema identifica documentos e evita confundir com outras colunas numéricas/textuais.

### 1) Pré-processamento dos valores

Antes de validar qualquer valor, o sistema:

1. Converte para string
2. Remove tudo que não for dígito (`0-9`)
3. Trabalha apenas com a sequência numérica final

Exemplos:

- `"529.982.247-25"` → `52998224725`
- `"03.579.633/1878-39"` → `03579633187839`

Isso permite validar documentos com ou sem máscara.

### 2) Validação de CPF (11 dígitos)

Um CPF válido possui 9 dígitos base + 2 dígitos verificadores.

Regras aplicadas:

- Deve ter exatamente 11 dígitos
- Rejeita sequências repetidas (ex: `11111111111`)
- Valida os 2 dígitos verificadores por checksum módulo 11

#### Cálculo do 1º dígito verificador

- Multiplica os 9 primeiros dígitos pelos pesos `10..2`
- Soma os resultados
- Calcula `resto = soma % 11`
- Dígito esperado:
    - `0`, se `resto < 2`
    - `11 - resto`, caso contrário

#### Cálculo do 2º dígito verificador

- Multiplica os 10 primeiros dígitos (incluindo o 1º DV) pelos pesos `11..2`
- Repete a mesma regra de módulo 11

Se os dois dígitos baterem, o CPF é considerado válido.

### 3) Validação de CNPJ (14 dígitos)

Um CNPJ válido possui 12 dígitos base + 2 dígitos verificadores.

Regras aplicadas:

- Deve ter exatamente 14 dígitos
- Rejeita sequências repetidas (ex: `00000000000000`)
- Valida os 2 dígitos verificadores por checksum módulo 11

#### Cálculo do 1º dígito verificador

- Usa os pesos: `5,4,3,2,9,8,7,6,5,4,3,2`
- Multiplica os 12 dígitos pelos pesos e soma
- Calcula `resto = soma % 11`
- Dígito esperado:
    - `0`, se `resto < 2`
    - `11 - resto`, caso contrário

#### Cálculo do 2º dígito verificador

- Usa os pesos: `6,5,4,3,2,9,8,7,6,5,4,3,2`
- Repete a mesma regra de módulo 11

Se os dois dígitos baterem, o CNPJ é considerado válido.

### 4) Como identifica colunas completas

Para cada coluna, o sistema avalia até `AMOSTRA` linhas e mede a taxa de valores válidos.

- Se a taxa de CPF válido ≥ `CONFIANCA`, marca coluna como CPF
- Se a taxa de CNPJ válido ≥ `CONFIANCA`, marca coluna como CNPJ

Com padrão atual:

- `AMOSTRA = 100`
- `CONFIANCA = 0.7`

Ou seja: precisa de pelo menos 70% de valores válidos na amostra.

### 5) Como valida prefixo/sufixo/partes (ex: raiz + sufixo + dígito)

Quando um documento está quebrado, o sistema tenta recompor automaticamente:

1. Seleciona colunas candidatas com conteúdo majoritariamente numérico (1 a 14 dígitos)
2. Testa combinações de 2 e 3 colunas
3. Concatena na ordem da combinação
4. Valida o resultado como CPF e CNPJ
5. Se atingir confiança ≥ 70%, marca o grupo como documento válido

Exemplos que ele consegue detectar:

- `cnpj_raiz + cnpj_complemento`
- `cnpj_raiz_unhash + cnpj_sufx + cnpj_dig`
- Outros nomes equivalentes, desde que o conteúdo forme documento válido

### 6) Como evita confundir com colunas numéricas comuns

O sistema não se baseia só em “parece número”. Ele exige validação matemática e taxa mínima.

Uma coluna como `id`, `valor`, `ano`, `cep` geralmente NÃO passa porque:

- Não tem tamanho/documento consistente
- Não passa no checksum de CPF/CNPJ
- Não atinge taxa mínima de 70% de válidos

Em resumo: o filtro é por **estrutura + checksum + confiança estatística**.

### 7) Fluxo final de preservação

1. Detecta colunas com CPF/CNPJ completos
2. Detecta grupos de colunas que formam documentos
3. Une tudo em `cols_preservar`
4. Preserva essas colunas sem alteração
5. Fakeia somente o restante

Resultado: preserva documentos sensíveis com precisão e reduz falsos positivos em colunas comuns.

## 🎯 Padrões Suportados

| Tipo | Exemplo | Status |
|------|---------|--------|
| CPF completo | `cpf`, `documento`, `ndoc_completo` | ✅ |
| CNPJ completo | `cnpj`, `cnpj_completo` | ✅ |
| CNPJ 2 partes | `cnpj_raiz` + `cnpj_complemento` | ✅ |
| CNPJ 3 partes | `doc_parte1` + `doc_parte2` + `doc_parte3` | ✅ |

**Não depende do nome** - valida por checksum algorítmico (70%+ valores válidos).

## 📊 Exemplo

**Original** (`fornecedores.csv`):
```csv
id,razao_social,cnpj,email
1,Empresa ABC,03579633187839,contato@abc.com
```

**Fake** (`fornecedores_fake.csv`):
```csv
id,razao_social,cnpj,email
id_3006,Empresa 5669,03579633187839,user742@yahoo.com.br
```

✅ CNPJ preservado | 🎭 Resto fakeado

## ⚙️ Configurações

Em `validar_documentos.py`:
```python
AMOSTRA = 100      # Linhas analisadas
CONFIANCA = 0.7    # Taxa mínima (70%) para considerar coluna
```

## 📁 Estrutura

```
projeto/
├── validar_documentos.py # Validação CPF/CNPJ
├── gerar_tabelas.py    # Gera dados de teste
├── fakear_tabelas.py   # Gera dados fake
└── dados/
    ├── original/       # CSVs originais
    └── fake/           # CSVs fakeados
```