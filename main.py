from playwright.sync_api import sync_playwright
from time import sleep
import json

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
    lista_responsabilidades = []
    for i in range(elementos.count()):
        texto = elementos.nth(i).text_content()
        if texto.strip():
            lista_responsabilidades.append(texto.strip())
    return lista_responsabilidades


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
    for vaga in dados_extraidos:
        link = vaga["link"]
        page.goto(link, wait_until="domcontentloaded")
        h2_responsabilidade = page.get_by_role("heading", name="Responsabilidades e atribuições")
        if h2_responsabilidade.count() > 0:
            div_responsabilidades = h2_responsabilidade.locator("xpath=..").locator("div")
            if div_responsabilidades.locator("ul").count() > 0:
                elementos = div_responsabilidades.locator("ul")
                vaga["responsabilidades"] = extrair_topicos(elementos)
            elif div_responsabilidades.locator("p").count() > 0:
                elementos = div_responsabilidades.locator("p")
                vaga["responsabilidades"] = extrair_topicos(elementos)
            sleep(3)
        else:
            vaga["responsabilidades"] = ["Ausente"]

        h2_requisitos = page.get_by_role("heading", name="Requisitos e qualificações")
        if h2_requisitos.count() > 0:
            div_requisitos = h2_requisitos.locator("xpath=..").locator("div")
            if div_requisitos.locator("ul").count() > 0:
                elementos = div_requisitos.locator("ul")
                vaga["requisitos"] = extrair_topicos(elementos)
            elif div_requisitos.locator("p").count() > 0:
                elementos = div_requisitos.locator("p")
                vaga["requisitos"] = extrair_topicos(elementos)
            sleep(3)
        else:
            vaga["requisitos"] = ["Ausente"]
        with open("vagas.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados_extraidos, arquivo, ensure_ascii=False, indent=4)
    print("Arquivo 'vagas.json' criado com sucesso!")



