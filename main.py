from playwright.sync_api import sync_playwright, Page
from time import sleep
import json
from datetime import datetime

def extrair_dados(cards) -> list:
    lista = []
    for i in range(cards.count()):
        card = cards.nth(i)
        titulo = card.locator("h3")
        empresa = card.locator("p").first
        link = card.get_attribute("href")
        lista.append({
            "titulo": titulo.text_content(),
            "empresa": empresa.text_content(),
            "link": link
        })
    return lista


def extrair_topicos(elementos) -> list:
    lista_textos = []
    for i in range(elementos.count()):
        texto = elementos.nth(i).text_content()
        if texto.strip():
            lista_textos.append(texto.strip())
    return lista_textos


def extrair_secao(page: Page, titulo_secao) -> list:
    h2 = page.get_by_role("heading", name=titulo_secao)

    if h2.count() > 0:
        div_conteudo = h2.locator("xpath=..").locator("div")

        if div_conteudo.locator("ul").count() > 0:
            return extrair_topicos(div_conteudo.locator("ul").locator("li"))
        elif div_conteudo.locator("p").count() > 0:
            return extrair_topicos(div_conteudo.locator("p"))
        else:
            return ["Estrutura de texto não reconhecida"]
    return ["Seção não estruturada ou ausente na vaga"]


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(channel="chrome", headless=False)
    page = browser.new_page()
    page.goto("https://portal.gupy.io/job-search/sortBy=publishedDate")
    page.locator("input[name='searchTerm']").first.type("Sistemas", delay=100)
    page.keyboard.press("Enter")
    page.get_by_test_id("KeyboardArrowDownRoundedIcon").nth(2).click()
    page.locator("input[type='checkbox'][name='remote']").check()
    page.get_by_role("button", name="Aplicar").click()
    page.locator("a[aria-label*='Ir para vaga']").first.wait_for()
    links_vagas = page.locator("a[aria-label*='Ir para vaga']")
    dados_extraidos = extrair_dados(links_vagas)

    vagas_unicas = []
    chaves_vistas = set()

    for vaga in dados_extraidos:
        chave = f"{vaga['titulo']} | {vaga['empresa']}"

        if chave not in chaves_vistas:
            vagas_unicas.append(vaga)
            chaves_vistas.add(chave)

    print(f"Total de vagas capturadas: {len(dados_extraidos)}")
    print(f"Vagas únicas após o filtro: {len(chaves_vistas)}")
    print("-"*40)

    for vaga in vagas_unicas:
        page.goto(vaga["link"], wait_until="domcontentloaded")
        vaga["responsabilidades"] = extrair_secao(page, "Responsabilidades e atribuições")
        vaga["requisitos"] = extrair_secao(page, "Requisitos e qualificações")

    data_hora = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"vagas_{data_hora}.json"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(vagas_unicas, arquivo, ensure_ascii=False, indent=4)
    print(f"Arquivo '{nome_arquivo}' criado com sucesso!")



