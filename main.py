from playwright.sync_api import sync_playwright, Page
from scraper import extrair_secao, extrair_dados
from utils import salvar_arquivo
from db import criar_tabela, salvar_no_banco

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(channel="chrome", headless=False)
    page = browser.new_page()
    page.goto("https://portal.gupy.io/job-search/sortBy=publishedDate")
    page.locator("input[name='searchTerm']").first.type("TI", delay=100)
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
        chave = f"{vaga['titulo']} | {vaga['empresa']} | {vaga['data_publicacao']}"

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

    salvar_arquivo(vagas_unicas)
    criar_tabela()
    salvar_no_banco(vagas_unicas)