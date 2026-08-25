from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus, urljoin, urlparse

import pandas as pd
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, sync_playwright

ARQUIVO_ENTRADA = Path("data/links.csv")
ARQUIVO_SAIDA = Path("data/precos_coletados.csv")
TIMEOUT_MS = 45_000
TENTATIVAS = 3

PAGINAS_DE_BUSCA = {
    "KaBuM": "https://www.kabum.com.br/busca/{consulta}",
    "Pichau": "https://www.pichau.com.br/search?q={consulta}",
    "TerabyteShop": "https://www.terabyteshop.com.br/busca?str={consulta}",
    "Mercado Livre": "https://lista.mercadolivre.com.br/{consulta}",
    "Amazon": "https://www.amazon.com.br/s?k={consulta}",
}

SELETORES_PRECO = {
    "KaBuM": ["h4.finalPrice", "[data-testid='price-value']", ".finalPrice"],
    "Pichau": ["[data-cy='price']", ".jss40", ".price"],
    "TerabyteShop": ["#valVista", ".valVista", ".precoVista"],
    "Mercado Livre": ["meta[itemprop='price']", ".andes-money-amount__fraction"],
    "Amazon": [".a-price .a-offscreen", "#priceblock_ourprice", "#price_inside_buybox"],
    "AliExpress": ["[class*='price--currentPriceText']", "[class*='product-price-value']"],
}


def identificar_loja(link: str) -> str:
    dominio = urlparse(str(link)).netloc.lower().removeprefix("www.")
    lojas = {
        "pichau": "Pichau",
        "kabum": "KaBuM",
        "amazon": "Amazon",
        "amzn.to": "Amazon",
        "mercadolivre": "Mercado Livre",
        "meli.la": "Mercado Livre",
        "terabyteshop": "TerabyteShop",
        "aliexpress": "AliExpress",
    }
    return next((nome for trecho, nome in lojas.items() if trecho in dominio), "Loja não identificada")


def normalizar_url(link: str) -> str:
    link = str(link).strip()
    parsed = urlparse(link)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("URL inválida")
    return link


def limpar_preco(valor: object) -> float | None:
    texto = re.sub(r"[^\d,\.]", "", str(valor)).strip()
    if not texto:
        return None
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif texto.count(".") > 1:
        texto = texto.replace(".", "")
    try:
        preco = float(texto)
    except ValueError:
        return None
    return round(preco, 2) if 500 <= preco <= 30_000 else None


def extrair_json_ld(page: Page) -> float | None:
    for script in page.locator("script[type='application/ld+json']").all():
        try:
            dados = json.loads(script.text_content() or "{}")
        except (json.JSONDecodeError, PlaywrightTimeoutError):
            continue
        itens = dados if isinstance(dados, list) else [dados]
        for item in itens:
            if not isinstance(item, dict):
                continue
            candidatos = [item, item.get("offers", {})]
            if isinstance(item.get("@graph"), list):
                candidatos.extend(item["@graph"])
            for candidato in candidatos:
                if not isinstance(candidato, dict):
                    continue
                oferta = candidato.get("offers", candidato)
                if isinstance(oferta, list):
                    oferta = oferta[0] if oferta else {}
                if isinstance(oferta, dict):
                    preco = limpar_preco(oferta.get("price") or oferta.get("lowPrice"))
                    if preco:
                        return preco
    return None


def extrair_por_seletor(page: Page, loja: str) -> float | None:
    for seletor in SELETORES_PRECO.get(loja, []):
        try:
            elemento = page.locator(seletor).first
            if elemento.count() == 0:
                continue
            valor = elemento.get_attribute("content") or elemento.text_content()
            preco = limpar_preco(valor)
            if preco:
                return preco
        except PlaywrightTimeoutError:
            continue
    return None


def extrair_do_texto(page: Page) -> float | None:
    texto = page.locator("body").inner_text(timeout=10_000)
    encontrados = re.findall(r"R\$\s*\d{1,3}(?:\.\d{3})*,\d{2}", texto)
    precos = [preco for item in encontrados if (preco := limpar_preco(item))]
    return min(precos) if precos else None


def termos_relevantes(produto: str) -> set[str]:
    ignorar = {"geforce", "radeon", "intel", "placa", "video", "de", "oc", "rgb", "gb"}
    termos = set(re.findall(r"[a-z]+\d+[a-z]*|\d+gb|\d{4}", produto.lower()))
    termos.update(
        termo
        for termo in re.findall(r"[a-z0-9]+", produto.lower())
        if len(termo) >= 4 and termo not in ignorar
    )
    return termos


def descobrir_links(page: Page, produto: str, loja: str, limite: int = 2) -> list[str]:
    modelo_busca = PAGINAS_DE_BUSCA.get(loja)
    if not modelo_busca:
        return []

    consulta = quote_plus(produto)
    url_busca = modelo_busca.format(consulta=consulta)
    try:
        page.goto(url_busca, wait_until="domcontentloaded", timeout=TIMEOUT_MS)
        page.wait_for_timeout(2500)
    except Exception as erro:
        print(f"[BUSCA] Falha ao pesquisar {produto} em {loja}: {erro}")
        return []

    dominio_loja = urlparse(url_busca).netloc.lower().removeprefix("www.")
    termos = termos_relevantes(produto)
    candidatos: dict[str, int] = {}

    for ancora in page.locator("a[href]").all():
        try:
            href = urljoin(page.url, ancora.get_attribute("href") or "")
            parsed = urlparse(href)
            if parsed.scheme not in {"http", "https"}:
                continue
            dominio = parsed.netloc.lower().removeprefix("www.")
            if dominio != dominio_loja:
                continue
            texto = f"{ancora.inner_text()} {parsed.path}".lower()
            pontuacao = sum(1 for termo in termos if termo in texto)
            if pontuacao >= max(1, min(2, len(termos))):
                link_limpo = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                candidatos[link_limpo] = max(candidatos.get(link_limpo, 0), pontuacao)
        except Exception:
            continue

    ordenados = sorted(candidatos, key=lambda link: candidatos[link], reverse=True)
    return ordenados[:limite]


def coletar_preco(page: Page, link: str, loja: str) -> tuple[float | None, str, str]:
    ultimo_erro = "Preço não encontrado"
    for tentativa in range(1, TENTATIVAS + 1):
        try:
            resposta = page.goto(link, wait_until="domcontentloaded", timeout=TIMEOUT_MS)
            if resposta and resposta.status >= 400:
                raise RuntimeError(f"HTTP {resposta.status}")
            page.wait_for_timeout(1500 * tentativa)
            preco = extrair_json_ld(page) or extrair_por_seletor(page, loja) or extrair_do_texto(page)
            if preco:
                return preco, "ok", page.url
            ultimo_erro = "Preço não encontrado"
        except Exception as erro:
            ultimo_erro = str(erro).splitlines()[0][:180]
    return None, "erro", ultimo_erro


def carregar_links() -> pd.DataFrame:
    df = pd.read_csv(ARQUIVO_ENTRADA, sep=None, engine="python", encoding="utf-8-sig")
    df.columns = [str(col).strip().lower() for col in df.columns]
    if not {"produto", "link"}.issubset(df.columns):
        raise ValueError("data/links.csv deve conter as colunas produto e link")
    df = df.dropna(subset=["produto", "link"]).drop_duplicates(subset=["produto", "link"])
    df["link"] = df["link"].map(normalizar_url)
    if "loja" not in df.columns:
        df["loja"] = df["link"].map(identificar_loja)
    else:
        df["loja"] = df.apply(
            lambda row: str(row["loja"]).strip() if pd.notna(row["loja"]) and str(row["loja"]).strip() else identificar_loja(row["link"]),
            axis=1,
        )
    return df


def main() -> None:
    resultados = []
    df_links = carregar_links()
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        contexto = navegador.new_context(
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
        )
        page = contexto.new_page()
        for row in df_links.itertuples(index=False):
            loja = str(row.loja)
            print(f"[PESQUISANDO] {row.produto} | {loja}")
            links_candidatos = [row.link]
            links_candidatos.extend(
                link
                for link in descobrir_links(page, row.produto, loja)
                if link not in links_candidatos
            )

            ofertas = []
            erros = []
            for link_candidato in links_candidatos:
                preco, status, detalhe = coletar_preco(page, link_candidato, loja)
                if status == "ok" and preco:
                    ofertas.append((preco, detalhe))
                    print(f"[OFERTA] R$ {preco:.2f} | {detalhe}")
                else:
                    erros.append(detalhe)

            if ofertas:
                preco, link_final = min(ofertas, key=lambda oferta: oferta[0])
                status = "ok"
                detalhe = link_final
            else:
                preco = None
                status = "erro"
                detalhe = " | ".join(erros[-2:])[:360] or "Nenhuma oferta válida encontrada"

            resultados.append({
                "produto": row.produto,
                "link": detalhe if status == "ok" else row.link,
                "link_final": detalhe if status == "ok" else "",
                "loja": loja,
                "preco": preco,
                "status": status,
                "erro": "" if status == "ok" else detalhe,
                "data_coleta": datetime.now().astimezone().isoformat(timespec="minutes"),
            })
            print(f"[{status.upper()}] {preco if preco else detalhe}")
        navegador.close()
    ARQUIVO_SAIDA.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(resultados).to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8-sig")
    sucessos = sum(item["status"] == "ok" for item in resultados)
    print(f"[RESUMO] {sucessos}/{len(resultados)} preços coletados")
    if sucessos == 0:
        raise SystemExit("Nenhum preço pôde ser coletado")


if __name__ == "__main__":
    main()

