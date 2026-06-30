from datetime import datetime
import json

def salvar_arquivo(lista_vagas):
    data_hora = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"vagas_{data_hora}.json"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(lista_vagas, arquivo, ensure_ascii=False, indent=4)
    print(f"Arquivo '{nome_arquivo}' criado com sucesso!")