
import os

target_file = r"e:\Projetos\sam_analise_financeira\notebooks\ypynb\celulas\PAGINA_3_FINANCEIRO.py"

replacements = {
    '🟢': '[OK]',
    '🟡': '[ATENCAO]',
    '🔴': '[ALERTA]',
    '💡': '',
    '⚠️': '[AVISO]',
    '🔹': '>',
    '🏆': '',
    '🔍': '',
    '💸': '',
    '📊': '',
    '📉': '',
    '📈': '',
    '💰': '',
    '🏦': '',
    '🚀': '',
    '✅': '[OK]',
    '❌': '[ERRO]'
}

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

for emoji, text in replacements.items():
    content = content.replace(emoji, text)

# Also removing non-ascii just in case, but preserving accents? 
# Better not aggressive strip, just the specific list + ensuring encoding is utf-8
# because portuguese accents are non-ascii.

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Emojis replaced successfully.")
