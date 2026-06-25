from playwright.sync_api import sync_playwright


def extrair_titulo(cards):
    lista = []
    for i in range(cards.count()):
        titulo = cards.nth(i).locator("h3")
        empresa = cards.nth(i).locator("p").first
        lista.append({
            "titulo": titulo.text_content(),
            "empresa": empresa.text_content()
        })
    return lista


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
    dados_extraidos = extrair_titulo(links_vagas)
    print(dados_extraidos)

    input()



