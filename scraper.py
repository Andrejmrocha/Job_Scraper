from playwright.sync_api import Page
from ia import refinar_com_ia
from utils import padronizar_data

def extrair_dados(cards) -> list:
    lista = []
    for i in range(cards.count()):
        card = cards.nth(i)
        titulo = card.locator("h3")
        empresa = card.locator("p").first
        data_publicacao = card.locator("p").nth(1).text_content()[-10:]
        link = card.get_attribute("href")
        lista.append({
            "titulo": titulo.text_content(),
            "empresa": empresa.text_content(),
            "link": link,
            "data_publicacao": padronizar_data(data_publicacao)
        })
    return lista


def extrair_topicos(elementos, titulo_secao) -> list:
    lista_textos = []
    for i in range(elementos.count()):
        texto = elementos.nth(i).text_content()
        if texto.strip():
            lista_textos.append(texto.strip())
    lista_refinada = refinar_com_ia(lista_textos, titulo_secao)
    return lista_refinada


def extrair_secao(page: Page, titulo_secao) -> list:
    h2 = page.get_by_role("heading", name=titulo_secao)

    if h2.count() > 0:
        div_conteudo = h2.locator("xpath=..").locator("div")

        if div_conteudo.locator("ul").count() > 0:
            return extrair_topicos(div_conteudo.locator("ul").locator("li"), titulo_secao)
        elif div_conteudo.locator("p").count() > 0:
            return extrair_topicos(div_conteudo.locator("p"), titulo_secao)
        else:
            return ["Estrutura de texto não reconhecida"]
    return ["Seção não estruturada ou ausente na vaga"]