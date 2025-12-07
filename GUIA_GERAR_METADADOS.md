# 📋 GUIA COMPLETO: GERAR METADADOS DO NOTEBOOK

## 🎯 Objetivo

Gerar **dois arquivos JSON** que documentam **todas as colunas, valores e estrutura** do notebook `real_vs_ideal.ipynb`:

1. **`METADADOS_NOTEBOOK_COMPLETO.json`** → Dados completos (colunas, valores M1/M36, estatísticas)
2. **`COLUNAS_DETALHADAS.json`** → Apenas colunas por célula (mais simples, fácil de ler)

---

## 📌 Você DELETOU CÉLULAS - COMO PROCEDER

Como você apagou algumas células, siga este passo a passo:

### **PASSO 1: Execute o Notebook Novamente**

Execute todas as células do notebook NA ORDEM, até que as variáveis sejam criadas:

- ✅ Célula 1: Setup & Imports
- ✅ Célula 2: PREMISSAS
- ⚠️ Célula 3: Diagnóstico (opcional)
- ✅ Célula 4: Motor Financeiro
- ⚠️ Célula 5: Cenário Real (DELETE ESTA CÉLULA? Precisa ser criada)
- ⚠️ Célula 6: Cenário Ideal (DELETE ESTA CÉLULA? Precisa ser criada)
- ⚠️ Célula 7: Monte Carlo (DELETE ESTA CÉLULA? Precisa ser criada)
- ⚠️ Célula 8: Análise Comparativa (DELETE ESTA CÉLULA? Precisa ser criada)
- ⚠️ Célula 9: Auditoria Forense (DELETE ESTA CÉLULA? Precisa ser criada)

**Resultado esperado:** As seguintes variáveis devem existir em memória:
```python
PREMISSAS          # Dict com 150+ chaves
df_real_m          # DataFrame mensal 36 linhas
df_real_a          # DataFrame anual 3 linhas
met_real           # Dict com KPIs
alertas_real       # Lista com alertas

df_ideal           # DataFrame mensal 36 linhas
df_ideal_anual     # DataFrame anual 3 linhas
met_ideal          # Dict com KPIs
alertas_ideal      # Lista com alertas

mc_results         # DataFrame 1500 linhas (500 sims × 3 cenários)
mc_errors          # DataFrame com erros
mc_data            # Dict com resumo
```

---

### **PASSO 2: Copie o Código do Extrator**

O arquivo `GERAR_METADADOS.py` contém um gerador completo. Ele já foi adicionado como célula ao final do notebook.

**OU manualmente:** copie e cole como uma célula Python no fim do seu notebook:

```python
# Cole aqui o conteúdo de GERAR_METADADOS.py
```

---

### **PASSO 3: Execute a Célula de Extração**

Após executar as células 5-9 (que criam as variáveis), execute a célula de extração:

```
🔍 INICIANDO EXTRAÇÃO DE METADADOS...

1️⃣  Detectando variáveis...
   ✅ df_real_m
   ✅ df_real_a
   ✅ met_real
   ✅ alertas_real
   ✅ df_ideal
   ✅ df_ideal_anual
   ✅ met_ideal
   ✅ alertas_ideal
   ✅ mc_results
   ✅ mc_data
   ✅ PREMISSAS

💾 Salvando arquivos JSON...
   ✅ METADADOS_NOTEBOOK_COMPLETO.json
   ✅ COLUNAS_DETALHADAS.json

✅ EXTRAÇÃO CONCLUÍDA!
```

---

### **PASSO 4: Localize os Arquivos Gerados**

Após a execução, você terá **2 novos arquivos JSON** no **diretório do notebook** (`notebooks/`):

```
📁 notebooks/
├── real_vs_ideal.ipynb
├── METADADOS_NOTEBOOK_COMPLETO.json  ← NOVO
├── COLUNAS_DETALHADAS.json           ← NOVO
├── extrator_metadados.py
├── GERAR_METADADOS.py
└── ...
```

---

## 📂 ESTRUTURA DOS ARQUIVOS GERADOS

### **`METADADOS_NOTEBOOK_COMPLETO.json`** (Arquivo Completo)

```json
{
  "data_extracao": "2025-12-05T10:30:00",
  "variaveis_encontradas": {
    "df_real_m": true,
    "df_ideal": true,
    "mc_results": true,
    "PREMISSAS": true,
    ...
  },
  "dataframes_detalhados": {
    "df_real_m": {
      "celula": 5,
      "shape": [36, 108],
      "num_linhas": 36,
      "num_colunas": 108,
      "colunas": [
        "mes", "trafego_total", "usuarios_ativos", "mrr", 
        "caixa", "burn_rate", "runway_meses", ...
      ],
      "tipos_colunas": {
        "mes": "int64",
        "mrr": "float64",
        "usuarios_ativos": "float64",
        ...
      },
      "valores_primeira_linha": {
        "mes": 1,
        "mrr": 950.0,
        "usuarios_ativos": 5.0,
        ...
      },
      "valores_ultima_linha": {
        "mes": 36,
        "mrr": 112822.5,
        "usuarios_ativos": 1269.0,
        ...
      },
      "stats": {
        "mrr": {
          "min": 950.0,
          "max": 112822.5,
          "mean": 45000.0,
          "std": 35000.0
        },
        ...
      }
    },
    "mc_results": {
      "celula": 7,
      "shape": [1500, 22],
      "colunas": [
        "simulacao_id", "cenario", "mrr_final_p50", "runway_p50", ...
      ],
      ...
    }
  },
  "resumo_executivo": {
    "cenario": "Real (Bootstrap)",
    "periodo_meses": 36,
    "metricas_m1": {
      "mrr": 950.0,
      "usuarios_ativos": 5.0,
      "caixa": 20000.0
    },
    "metricas_m36": {
      "mrr": 112822.5,
      "usuarios_ativos": 1269.0,
      "caixa": 185443.0,
      "churn_rate": 0.07,
      "ltv_cac": 5.1,
      "runway_meses": 999
    }
  }
}
```

### **`COLUNAS_DETALHADAS.json`** (Arquivo Simplificado)

```json
{
  "metadata": {
    "data": "2025-12-05T10:30:00",
    "objetivo": "Mapa de todas as colunas geradas por cada célula"
  },
  "celulas": {
    "celula_5_df_real_m": {
      "celula_numero": 5,
      "celula_nome": "Execução Cenário Real",
      "variavel_saida": "df_real_m",
      "num_colunas": 108,
      "colunas": [
        "mes", "trafego_total", "novos_pagantes_total", "usuarios_ativos",
        "mrr", "arr", "arpu", "receita_bruta", "receita_liquida",
        "cogs_total", "margem_bruta", "margem_bruta_pct",
        "opex_total", "ebitda", "lucro_liquido",
        "caixa", "burn_rate", "runway_meses",
        "cac_blended", "ltv", "ltv_cac", "churn_rate",
        ...
      ]
    },
    "celula_6_df_ideal": {
      "celula_numero": 6,
      "celula_nome": "Cenário Ideal",
      "variavel_saida": "df_ideal",
      "num_colunas": 108,
      "colunas": [...]
    },
    "celula_7_mc_results": {
      "celula_numero": 7,
      "celula_nome": "Monte Carlo Enterprise",
      "variavel_saida": "mc_results",
      "num_colunas": 22,
      "colunas": [
        "simulacao_id", "cenario", "seed",
        "mrr_final_p10", "mrr_final_p50", "mrr_final_p90",
        "usuarios_final_p10", "usuarios_final_p50", "usuarios_final_p90",
        "runway_p10", "runway_p50", "runway_p90",
        ...
      ]
    }
  }
}
```

---

## 🔍 COMO USAR OS JSONs

### **Opção 1: Análise Rápida (Excel/Sheets)**

1. Abra `COLUNAS_DETALHADAS.json` em um editor de texto
2. Copie o conteúdo
3. Paste em um Google Sheets ou Excel (menu "Dados" → "De Texto")
4. Pronto! Você tem uma tabela com todas as colunas por célula

### **Opção 2: Análise Programática (Python)**

```python
import json

# Carregar metadados
with open('METADADOS_NOTEBOOK_COMPLETO.json') as f:
    metadata = json.load(f)

# Ver todas as colunas de df_real_m
colunas_reais = metadata['dataframes_detalhados']['df_real_m']['colunas']
print(f"df_real_m tem {len(colunas_reais)} colunas:")
print(colunas_reais)

# Ver valores no mês 36
valores_m36 = metadata['dataframes_detalhados']['df_real_m']['valores_ultima_linha']
print(f"MRR no mês 36: R$ {valores_m36['mrr']:,.2f}")
print(f"Usuários no mês 36: {valores_m36['usuarios_ativos']}")
```

### **Opção 3: Sincronizar com Builders**

Use `COLUNAS_DETALHADAS.json` para atualizar a documentação dos builders:

```
✅ Cada célula retorna um DataFrame com X colunas
✅ Compare com a estrutura esperada dos builders
✅ Identifique gaps (colunas faltando ou a mais)
```

---

## 🚨 TROUBLESHOOTING

### **Erro: "❌ df_real_m (não encontrada)"**

**Causa:** A célula 5 (Execução Cenário Real) não foi executada ou foi deletada.

**Solução:**
1. Verifique se a célula 5 existe no notebook
2. Se não existir, você precisa recriá-la (rodar motor com `executar_motor_fintech_v10_production_ready()`)
3. Certifique-se de executar a célula 4 (Motor) ANTES da célula 5

### **Erro: "PREMISSAS não está em globals()"**

**Causa:** A célula 2 não foi executada.

**Solução:** Execute a célula 2 do notebook primeiro.

### **Arquivo JSON vazio ou com pouco conteúdo**

**Causa:** Nem todas as células foram executadas.

**Solução:**
1. Execute as células NA ORDEM: 1 → 2 → 4 → 5 → 6 → 7 → 8 → 9 → Extrator
2. Não pule nenhuma (exceto a célula 3 que é opcional)

---

## 📊 PRÓXIMOS PASSOS

Após gerar os JSONs:

1. **Atualize `ANALISE_NOTEBOOK_ESTRUTURA.json`** com as colunas reais
2. **Compare com `core/builders/`** para sincronizar a estrutura
3. **Use para documentação** de APIs/dashboards
4. **Valide** se todas as colunas esperadas existem

---

## 🎓 RESUMO RÁPIDO

| Passo | O que fazer | Arquivo |
|-------|-----------|---------|
| 1️⃣ | Execute todas as células | `real_vs_ideal.ipynb` |
| 2️⃣ | Cole `GERAR_METADADOS.py` como célula | `notebooks/GERAR_METADADOS.py` |
| 3️⃣ | Execute a célula do extrator | (no notebook) |
| 4️⃣ | Localize os JSONs gerados | `notebooks/METADADOS_NOTEBOOK_COMPLETO.json` |
| 5️⃣ | Use para sincronizar/documentar | Seus arquivos de documentação |

---

**Dúvidas?** Verifique os erros na saída da célula de extração. O script é bem documentado e mostra exatamente o que encontrou/não encontrou.
