from playwright.sync_api import sync_playwright


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


def extrair_responsabilidades(unordered_list) -> list:
    lista_responsabilidades = []
    topicos = unordered_list.locator("li")
    for i in range(topicos.count()):
        texto = topicos.nth(i)
        lista_responsabilidades.append(texto.text_content())
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
    vaga = dados_extraidos[0]
    link = vaga["link"]
    page.goto(link)
    h2_responsabilidade = page.get_by_role("heading", name="Responsabilidades e atribuições")
    div_responsabilidades = h2_responsabilidade.locator("xpath=..").locator("div")
    lista_ul = div_responsabilidades.locator("ul")
    responsabilidades = extrair_responsabilidades(lista_ul)
    for responsabilidade in responsabilidades:
        print(responsabilidade)
    input()



