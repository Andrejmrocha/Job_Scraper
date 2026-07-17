from playwright.sync_api import sync_playwright, Page
from scraper import extrair_secao, extrair_dados
from utils import salvar_arquivo
from db import criar_tabela, salvar_no_banco, obter_chaves_existentes
from ia import determinar_senioridade_com_ia
import sys

termos_busca = ["TI", "Sistemas", "Dados", "RPA", "Desenvolvedor"]

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(channel="chrome", headless=False)
    page = browser.new_page()

    todas_vagas = []

    for termo in termos_busca:
        page.goto("https://portal.gupy.io/job-search/sortBy=publishedDate")
        page.locator("input[placeholder='Busque por nome da vaga']").first.fill(termo)
        page.keyboard.press("Enter")

        page.get_by_test_id("KeyboardArrowDownRoundedIcon").nth(2).click()
        page.locator("input[type='checkbox'][name='remote']").check()
        page.get_by_role("button", name="Aplicar").click()

        page.locator("a[aria-label*='Ir para vaga']").first.wait_for()
        links_vagas = page.locator("a[aria-label*='Ir para vaga']")
        dados_extraidos = extrair_dados(links_vagas)
        todas_vagas.extend(dados_extraidos)

    vagas_novas = []
    chaves_vistas = obter_chaves_existentes()
    historico_tamanho = len(chaves_vistas)

    for vaga in todas_vagas:
        chave = f"{vaga['titulo']} | {vaga['empresa']} | {vaga['data_publicacao']}"
        if chave not in chaves_vistas:
            vagas_novas.append(vaga)
            chaves_vistas.add(chave)

    print(f"Total de vagas capturadas: {len(todas_vagas)}")
    print(f"Vagas novas: {len(vagas_novas)}")
    print("-"*40)

    if len(vagas_novas) == 0:
        print("Sem vagas novas no momento!")
        sys.exit(0)

    for vaga in vagas_novas:
        page.goto(vaga["link"], wait_until="domcontentloaded")
        vaga["responsabilidades"] = extrair_secao(page, "Responsabilidades e atribuições")
        vaga["requisitos"] = extrair_secao(page, "Requisitos e qualificações")
        vaga["senioridade"] = determinar_senioridade_com_ia(vaga["titulo"], vaga["requisitos"])

    salvar_arquivo(vagas_novas)
    criar_tabela()
    salvar_no_banco(vagas_novas)