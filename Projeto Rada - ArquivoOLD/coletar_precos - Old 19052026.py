import re
import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright

ARQUIVO_ENTRADA = "data/links.csv"
ARQUIVO_SAIDA = "data/precos_coletados.csv"


def identificar_loja(link):
    link = str(link).lower()

    if "pichau" in link:
        return "Pichau"
    if "kabum" in link:
        return "KaBuM"
    if "amazon" in link or "amzn.to" in link:
        return "Amazon"
    if "mercadolivre" in link or "meli.la" in link:
        return "Mercado Livre"
    if "terabyte" in link:
        return "Terabyte"
    if "terabyte" in link:
        return "AliExpress"

    return "Loja não identificada"


def limpar_preco(texto):
    texto = str(texto)
    texto = texto.replace("R$", "")
    texto = texto.replace(".", "")
    texto = texto.replace(",", ".")
    texto = texto.strip()

    try:
        return float(texto)
    except Exception:
        return 0.00


def extrair_preco(texto):
    padrao = r"R\$\s?\d{1,3}(?:\.\d{3})*,\d{2}"
    encontrados = re.findall(padrao, texto)

    precos = []

    for item in encontrados:
        preco = limpar_preco(item)

        if 300 <= preco <= 20000:
            precos.append(preco)

    if not precos:
        return 0.00

    return min(precos)


def coletar_preco(page, link):
    try:
        page.goto(link, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(7000)

        texto = page.inner_text("body")
        preco = extrair_preco(texto)

        return preco

    except Exception as erro:
        print(f"[ERRO] Falha ao coletar: {link}")
        print(erro)
        return 0.00


def carregar_links():
    df = pd.read_csv(
        ARQUIVO_ENTRADA,
        sep=None,
        engine="python",
        encoding="latin1"
    )

    df.columns = [col.strip().lower() for col in df.columns]

    if "produto" not in df.columns:
        raise Exception("A coluna 'produto' não existe no arquivo data/links.csv")

    if "link" not in df.columns:
        raise Exception("A coluna 'link' não existe no arquivo data/links.csv")

    if "loja" not in df.columns:
        df["loja"] = df["link"].apply(identificar_loja)

    return df


def main():
    df_links = carregar_links()

    resultados = []

    with sync_playwright() as p:
        navegador = p.chromium.launch(
            headless=True
        )

        page = navegador.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )

        for _, row in df_links.iterrows():
            produto = row["produto"]
            link = row["link"]
            loja = row["loja"] if pd.notna(row["loja"]) else identificar_loja(link)

            print("=" * 60)
            print(f"[COLETANDO] {produto}")
            print(f"[LOJA] {loja}")
            print(f"[LINK] {link}")

            preco = coletar_preco(page, link)

            print(f"[PREÇO] R$ {preco}")

            resultados.append({
                "produto": produto,
                "link": link,
                "loja": loja,
                "preco": preco,
                "data_coleta": datetime.now().strftime("%d/%m/%Y %H:%M")
            })

        navegador.close()

    df_resultado = pd.DataFrame(resultados)

    df_resultado.to_csv(
        ARQUIVO_SAIDA,
        index=False,
        encoding="utf-8-sig"
    )

    print("=" * 60)
    print("[OK] COLETA FINALIZADA")
    print(f"Arquivo salvo em: {ARQUIVO_SAIDA}")
    print("=" * 60)


if __name__ == "__main__":
    main()
