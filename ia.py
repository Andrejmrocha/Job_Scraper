import json
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

cliente = OpenAI(api_key=api_key)

def refinar_com_ia(lista_original, tipo_secao) -> list:
    if not lista_original or lista_original[0] in ["Seção não estruturada ou ausente na vaga",
                                                   "Estrutura de texto não reconhecida"]:
        return lista_original

    texto_bruto = "\n".join(lista_original)

    prompt = f"""
    Você é um engenheiro de dados limpando informações de vagas de TI.
    O texto abaixo refere-se à seção '{tipo_secao}'.
    Sua missão é organizar esse texto bruto em uma lista limpa de tópicos.

    REGRAS ABSOLUTAS:
    1. Corrija a formatação e elimine ruídos (ex: marcadores quebrados, títulos no meio do texto).
    2. NÃO resuma, NÃO exclua requisitos/responsabilidades reais e NÃO invente nada.
    3. Retorne EXCLUSIVAMENTE um objeto JSON no formato exato: {{"topicos": ["item 1", "item 2"]}}
    """
    try:
        response = cliente.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": texto_bruto}
            ],
            temperature=0.1
        )

        resposta_json = json.loads(response.choices[0].message.content)
        return resposta_json["topicos"]
    except Exception as e:
        print(f"Aviso: Erro ao processar {tipo_secao}. Erro: {e}")
        return lista_original