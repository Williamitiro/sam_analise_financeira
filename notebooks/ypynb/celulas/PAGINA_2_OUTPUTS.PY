# PAGINA 2 - OUTPUTS 
#  Importa (se não colou direto na célula) ou garante que as funções existem
# from notebooks.modelo2_v7 import executar_pagina_2_growth_machine  # Descomente se usar import

# EXECUÇÃO FINAL
executar_pagina_2_growth_machine(
    df_real_m=df_real_m,
    df_real_s=df_real_s,    # Garantir que rodou a Célula 5A que gera isso!
    df_ideal=df_ideal,      # Garantir que rodou a Célula 5B
    df_ideal_s=df_ideal_s,  # Garantir que rodou a Célula 5B
    premissas=PREMISSAS
)