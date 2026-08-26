import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from desempenho import (
    adicionar_indice_radar,
    carregar_base_tecnica,
    descrever_metodologia,
)

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Radar GPU Gamer BR",
    page_icon="🎮",
    layout="wide"
)

tema = st.sidebar.radio(
    "🎨 Tema",
    ["Escuro", "Claro"],
    horizontal=True,
    help="Altere a aparência do dashboard."
)
tema_claro = tema == "Claro"
cor_fundo = "#f8fafc" if tema_claro else "#020817"
cor_card = "#ffffff" if tema_claro else "#081226"
cor_texto = "#0f172a" if tema_claro else "#f8fafc"
cor_borda = "#dbe4f0" if tema_claro else "#1e293b"
cor_muted = "#64748b" if tema_claro else "#94a3b8"
cor_hover = "#f1f5f9" if tema_claro else "#111827"
cor_grid = "#e2e8f0" if tema_claro else "#1e293b"
plotly_template = "plotly_white" if tema_claro else "plotly_dark"

# ============================================================
# DESIGN SYSTEM
# ============================================================

st.markdown(f"""
<style>
:root {{
  --bg:{cor_fundo}; --card:{cor_card}; --text:{cor_texto};
  --muted:{cor_muted}; --border:{cor_borda}; --hover:{cor_hover};
  --primary:#6366f1; --cyan:#06b6d4; --green:#10b981;
}}
.stApp {{
  background:
    radial-gradient(circle at 90% -10%,rgba(99,102,241,.18),transparent 34rem),
    radial-gradient(circle at 5% 30%,rgba(6,182,212,.09),transparent 28rem),
    var(--bg);
  color:var(--text);
}}
.main .block-container {{max-width:1440px;padding:1.4rem 2rem 3rem}}
#MainMenu,footer{{visibility:hidden}}
header[data-testid="stHeader"]{{background:transparent}}
h1,h2,h3,h4,h5,h6,p,span,label{{color:var(--text)}}
section[data-testid="stSidebar"]{{
  background:color-mix(in srgb,var(--card) 94%,transparent);
  border-right:1px solid var(--border);
}}
section[data-testid="stSidebar"]>div{{padding-top:1.25rem}}
[data-baseweb="select"]>div,[data-testid="stTextInput"] input{{
  background:var(--card)!important;border-color:var(--border)!important;color:var(--text)!important
}}
[data-baseweb="tab-list"]{{
  gap:.4rem;background:var(--card);border:1px solid var(--border);
  border-radius:14px;padding:.35rem
}}
[data-baseweb="tab"]{{border-radius:10px;padding:.6rem 1rem}}
[data-baseweb="tab"][aria-selected="true"]{{background:linear-gradient(135deg,#6366f1,#4f46e5)}}
[data-baseweb="tab"][aria-selected="true"] p{{color:white!important}}
.radar-header{{
  position:relative;overflow:hidden;
  background:linear-gradient(120deg,#4338ca,#1d4ed8 58%,#0891b2);
  border:1px solid rgba(255,255,255,.18);border-radius:24px;
  padding:2rem 2.2rem;margin-bottom:1rem;box-shadow:0 24px 60px rgba(15,23,42,.22)
}}
.radar-header:after{{
  content:"";position:absolute;width:270px;height:270px;right:-70px;top:-120px;
  border-radius:50%;border:48px solid rgba(255,255,255,.08)
}}
.eyebrow{{color:#c7d2fe!important;font-size:.76rem;font-weight:800;letter-spacing:.14em}}
.radar-title{{
  color:white!important;font-size:clamp(2rem,4vw,3.25rem);line-height:1.02;
  font-weight:900;letter-spacing:-.045em;margin:.45rem 0 .65rem
}}
.radar-subtitle{{color:#e0e7ff!important;max-width:760px;line-height:1.6}}
.status-pill{{
  display:inline-flex;align-items:center;gap:.5rem;margin-top:1rem;padding:.45rem .75rem;
  border-radius:999px;background:rgba(15,23,42,.26);border:1px solid rgba(255,255,255,.2);
  color:white!important;font-size:.78rem;font-weight:750
}}
.status-dot{{width:8px;height:8px;border-radius:50%;background:#34d399;box-shadow:0 0 0 5px rgba(52,211,153,.16)}}
.section-title{{font-size:1.18rem;font-weight:850;letter-spacing:-.02em;margin:1.4rem 0 .25rem}}
.section-copy{{color:var(--muted)!important;font-size:.88rem;margin-bottom:.85rem}}
div[data-testid="stMetric"]{{
  background:linear-gradient(145deg,var(--card),var(--hover));border:1px solid var(--border);
  border-radius:18px;padding:1rem 1.1rem;box-shadow:0 10px 28px rgba(15,23,42,.06)
}}
div[data-testid="stMetric"] label{{color:var(--muted)!important;font-weight:700}}
div[data-testid="stMetricValue"]{{font-weight:900;letter-spacing:-.035em}}
div[data-testid="stVerticalBlockBorderWrapper"]{{
  background:var(--card);border-color:var(--border)!important;border-radius:18px;
  box-shadow:0 10px 30px rgba(15,23,42,.06)
}}
[data-testid="stDataFrame"]{{border:1px solid var(--border);border-radius:16px;overflow:hidden}}
.stButton>button,.stLinkButton>a{{border-radius:12px!important;min-height:2.65rem;font-weight:750!important}}
.stLinkButton>a{{background:linear-gradient(135deg,#4f46e5,#6366f1)!important;border:none!important;color:white!important}}
.offer-store{{color:#6366f1!important;font-size:.74rem;font-weight:900;letter-spacing:.09em;text-transform:uppercase}}
.offer-name{{font-size:1rem;font-weight:850;line-height:1.35;min-height:2.7rem;margin:.35rem 0 .65rem}}
.offer-price{{font-size:1.55rem;font-weight:900;letter-spacing:-.04em}}
.offer-meta{{color:var(--muted)!important;font-size:.77rem;margin:.35rem 0 .8rem}}
.sidebar-brand{{font-size:1.08rem;font-weight:900;letter-spacing:-.035em}}
.sidebar-copy{{color:var(--muted)!important;font-size:.78rem;line-height:1.5;margin:.15rem 0 1rem}}
@media(max-width:900px){{
  .main .block-container{{padding:.8rem .8rem 2rem}}
  .radar-header{{padding:1.4rem;border-radius:18px}}
}}
</style>
""",unsafe_allow_html=True)

# ============================================================
# BASE TÉCNICA DAS GPUS
# ============================================================

df_base = carregar_base_tecnica()

# ============================================================
# FUNÇÕES
# ============================================================

def formatar_moeda(valor):
    try:
        return (
            f"R$ {float(valor):,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
    except Exception:
        return "R$ 0,00"


def normalizar_preco(valor):
    if pd.isna(valor):
        return None

    valor = str(valor).strip().replace("R$", "").replace(" ", "")

    if "," in valor:
        valor = valor.replace(".", "").replace(",", ".")

    try:
        return float(valor)
    except Exception:
        return None


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
        return "TerabyteShop"
    if "ebay" in link:
        return "eBay"
    if "aliexpress" in link:
        return "AliExpress"

    return "Loja não identificada"


def identificar_gpu(produto, link):
    texto = f"{produto} {link}".lower()

    if "7600" in texto and "rx" in texto:
        return "Radeon RX 7600 8GB"
    if "6600" in texto and "rx" in texto:
        return "Radeon RX 6600 8GB"
    if "4060" in texto:
        return "GeForce RTX 4060 8GB"
    if "4070" in texto and "super" in texto:
        return "GeForce RTX 4070 SUPER 12GB"
    if "5060" in texto:
        return "GeForce RTX 5060 8GB"
    if "3060" in texto:
        return "GeForce RTX 3060 12GB"
    if "b580" in texto or "arc" in texto:
        return "Intel Arc B580 12GB"

    return produto


@st.cache_data(ttl=300)
def carregar_dados():
    # Altere esta chave quando o formato da coleta mudar.
    cache_version = "ofertas-multiloja-v1"
    caminho_csv = "data/precos_coletados.csv"

    df = df_base.copy()
    df["Origem_Preco"] = "Base fixa"
    df["Data_Coleta"] = pd.NaT
    df["Status_Link"] = "base"

    if not os.path.exists(caminho_csv):
        return df

    try:
        df_precos = pd.read_csv(
            caminho_csv,
            sep=None,
            engine="python",
            encoding="utf-8-sig",
            on_bad_lines="skip"
        )

        df_precos.columns = [
            str(col).strip().lower()
            for col in df_precos.columns
        ]

        df_precos = df_precos.rename(columns={
            "produto": "produto",
            "gpu": "produto",
            "link": "link",
            "url": "link",
            "loja": "loja",
            "site": "loja",
            "preco": "preco",
            "preço": "preco",
            "preco atual": "preco",
            "preço atual": "preco",
        })

        if not {"produto", "link", "preco"}.issubset(df_precos.columns):
            return df

        if "loja" not in df_precos.columns:
            df_precos["loja"] = df_precos["link"].apply(identificar_loja)

        if "data_coleta" not in df_precos.columns:
            df_precos["data_coleta"] = pd.NaT
        df_precos["data_coleta"] = pd.to_datetime(
            df_precos["data_coleta"],
            errors="coerce",
            utc=True
        )

        if "status" not in df_precos.columns:
            df_precos["status"] = "ok"

        df_precos["GPU"] = df_precos.apply(
            lambda row: identificar_gpu(row["produto"], row["link"]),
            axis=1
        )

        df_precos["Preco_Coletado"] = df_precos["preco"].apply(normalizar_preco)

        df_precos = df_precos[
            df_precos["Preco_Coletado"].notna() &
            (df_precos["Preco_Coletado"] > 0)
        ]

        if df_precos.empty:
            return df

        df_auto = df_precos[[
            "GPU",
            "loja",
            "link",
            "Preco_Coletado",
            "data_coleta",
            "status"
        ]].rename(columns={
            "loja": "Loja_Auto",
            "link": "Link_Auto",
            "data_coleta": "Data_Coleta_Auto",
            "status": "Status_Link_Auto"
        })

        df = pd.merge(
            df,
            df_auto,
            on="GPU",
            how="left"
        )

        df["Preco_Atual"] = df.apply(
            lambda row: row["Preco_Coletado"]
            if pd.notna(row.get("Preco_Coletado")) and row["Preco_Coletado"] > 0
            else row["Preco_Atual"],
            axis=1
        )

        df["Loja"] = df.apply(
            lambda row: row["Loja_Auto"]
            if pd.notna(row.get("Loja_Auto"))
            else row["Loja"],
            axis=1
        )

        df["Link"] = df.apply(
            lambda row: row["Link_Auto"]
            if pd.notna(row.get("Link_Auto"))
            else row["Link"],
            axis=1
        )

        df["Origem_Preco"] = df.apply(
            lambda row: "Automático"
            if pd.notna(row.get("Preco_Coletado")) and row["Preco_Coletado"] > 0
            else "Base fixa",
            axis=1
        )

        df["Data_Coleta"] = df["Data_Coleta_Auto"]
        df["Status_Link"] = df.apply(
            lambda row: row["Status_Link_Auto"]
            if pd.notna(row.get("Status_Link_Auto"))
            else "base",
            axis=1
        )

        colunas = df_base.columns.tolist() + [
            "Origem_Preco",
            "Data_Coleta",
            "Status_Link"
        ]
        return df[colunas]

    except Exception:
        return df


df = carregar_dados()

# ============================================================
# FILTROS E PROCESSAMENTO
# ============================================================

with st.sidebar:
    st.markdown('<div class="sidebar-brand">◈ Radar GPU</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-copy">Inteligência de preços e desempenho para sua próxima GPU.</div>',
        unsafe_allow_html=True
    )
    st.markdown("### Filtros")
    busca = st.text_input("GPU ou modelo", placeholder="RTX 4060, Radeon, ASRock...")
    marcas = st.multiselect("Marca", sorted(df["Marca"].dropna().unique().tolist()))
    lojas = st.multiselect("Loja", sorted(df["Loja"].dropna().unique().tolist()))
    vrams = st.multiselect(
        "Memória",
        sorted(df["VRAM"].dropna().astype(int).unique().tolist()),
        format_func=lambda valor: f"{valor} GB"
    )
    foco = st.selectbox(
        "Perfil de uso", ["Gamer 1080p", "Gamer 1440p", "Jogos + streaming"]
    )
    limite_preco = max(1000, int(df["Preco_Atual"].max() // 100 * 100 + 100))
    faixa_preco = st.slider(
        "Faixa de preço", 0, limite_preco, (0, limite_preco), 100, format="R$ %d"
    )
    origem = st.radio("Dados", ["Todas", "Automático", "Base fixa"], horizontal=True)
    ordenar_por = st.selectbox(
        "Ordenar", ["Melhor score", "Menor preço", "Maior FPS 1080p", "Maior desconto"]
    )
    st.divider()
    st.caption("Versão 4.1 • benchmarks rastreáveis")

df = adicionar_indice_radar(df, foco)
df_filtrado = df.copy()
if busca.strip():
    termo = busca.strip()
    df_filtrado = df_filtrado[
        df_filtrado["GPU"].astype(str).str.contains(termo, case=False, na=False, regex=False)
        | df_filtrado["Modelo"].astype(str).str.contains(termo, case=False, na=False, regex=False)
    ]
if marcas:
    df_filtrado = df_filtrado[df_filtrado["Marca"].isin(marcas)]
if lojas:
    df_filtrado = df_filtrado[df_filtrado["Loja"].isin(lojas)]
if vrams:
    df_filtrado = df_filtrado[df_filtrado["VRAM"].isin(vrams)]
df_filtrado = df_filtrado[
    df_filtrado["Preco_Atual"].between(faixa_preco[0], faixa_preco[1])
]
if origem != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Origem_Preco"] == origem]
if df_filtrado.empty:
    st.warning("Nenhuma GPU corresponde aos filtros atuais.")
    st.stop()

df_filtrado["Desconto_%"] = (
    ((df_filtrado["Preco_Antigo"] - df_filtrado["Preco_Atual"])
     / df_filtrado["Preco_Antigo"]) * 100
).clip(lower=0).round(1)
df_filtrado["Custo_por_FPS"] = (
    df_filtrado["Preco_Atual"] / df_filtrado["FPS_1080p"]
).round(2)

ordenacoes = {
    "Melhor score": ("Score", False),
    "Menor preço": ("Preco_Atual", True),
    "Maior FPS 1080p": ("FPS_1080p", False),
    "Maior desconto": ("Desconto_%", False),
}
coluna_ordem, ordem_crescente = ordenacoes[ordenar_por]
df_filtrado = df_filtrado.sort_values(coluna_ordem, ascending=ordem_crescente).reset_index(drop=True)
df_filtrado["#"] = df_filtrado.index + 1

datas_validas = pd.to_datetime(df_filtrado["Data_Coleta"], errors="coerce", utc=True).dropna()
if not datas_validas.empty:
    ultima_atualizacao = datas_validas.max().tz_convert("America/Sao_Paulo")
    texto_atualizacao = f"Atualizado {ultima_atualizacao:%d/%m às %H:%M}"
    horas_desde_coleta = (
        pd.Timestamp.now(tz="America/Sao_Paulo") - ultima_atualizacao
    ).total_seconds() / 3600
else:
    texto_atualizacao = "Aguardando coleta automática"
    horas_desde_coleta = 999

st.markdown(f"""
<div class="radar-header">
  <div class="eyebrow">GPU MARKET INTELLIGENCE</div>
  <div class="radar-title">Escolha melhor.<br>Pague menos.</div>
  <div class="radar-subtitle">
    Ofertas verificadas em lojas confiáveis, benchmarks raster e ray tracing
    com fonte publicada e um índice transparente para encontrar a GPU ideal.
  </div>
  <div class="status-pill"><span class="status-dot"></span>
    {texto_atualizacao} · {len(datas_validas)} ofertas verificadas
  </div>
</div>
""",unsafe_allow_html=True)

if horas_desde_coleta > 36:
    st.warning("A última coleta tem mais de 36 horas. Confirme preço e estoque na loja.")

benchmark_atualizado = df_base["Benchmark_Atualizado_Em"].max().strftime("%d/%m/%Y")
st.caption(
    "Desempenho: média de jogos em resolução nativa e preset Ultra, sem "
    f"upscaling ou geração de quadros · base consultada em {benchmark_atualizado}."
)
with st.expander("Como o desempenho e o Índice Radar são calculados"):
    st.markdown(
        f"**Perfil selecionado:** {descrever_metodologia(foco)}. "
        "Cada componente é normalizado entre as GPUs monitoradas; preço usa a "
        "oferta atual. Por isso, o índice pode mudar quando os preços mudam."
    )
    st.markdown(
        "**Fontes:** [GPU Hierarchy 2026 — resultados]"
        "(https://www.tomshardware.com/reviews/gpu-hierarchy%2C4388.html) · "
        "[metodologia e bancada de testes]"
        "(https://www.tomshardware.com/pc-components/gpus/"
        "the-great-bench-gpu-retest-begins-how-were-testing-for-our-gpu-"
        "hierarchy-in-2026-and-why-upscaling-and-framegen-are-still-out)."
    )
    st.info(
        "FPS são médias comparativas, não uma promessa para todos os jogos. "
        "CPU, drivers, memória, API gráfica e configurações alteram o resultado."
    )

aba_geral, aba_comparador, aba_ofertas = st.tabs(
    ["Visão geral", "Comparador", "Melhores ofertas"]
)

with aba_geral:
    melhor = df_filtrado.iloc[0]
    menor = df_filtrado.sort_values("Preco_Atual").iloc[0]
    desempenho = df_filtrado.sort_values("FPS_1080p", ascending=False).iloc[0]
    automaticas = int((df_filtrado["Origem_Preco"] == "Automático").sum())

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("GPUs no radar", len(df_filtrado), f"{automaticas} verificadas")
    k2.metric("Menor preço", formatar_moeda(menor["Preco_Atual"]), menor["GPU"])
    k3.metric("Melhor score", melhor["GPU"], f"{melhor['Score']:.1f} pontos")
    k4.metric(
        "Maior desempenho raster",
        f"{desempenho['FPS_1080p']:.1f} FPS",
        desempenho["GPU"],
    )

    st.markdown('<div class="section-title">Panorama do mercado</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Preço, desempenho e eficiência das opções filtradas.</div>', unsafe_allow_html=True)
    g1, g2 = st.columns([1.15, 1])

    with g1:
        fig_score = px.bar(
            df_filtrado.sort_values("Score"), x="Score", y="GPU", orientation="h",
            color="Score", color_continuous_scale=["#334155", "#6366f1", "#22d3ee"],
            template=plotly_template, text="Score"
        )
        fig_score.update_layout(
            title="Ranking inteligente", height=390, paper_bgcolor=cor_card,
            plot_bgcolor=cor_card, font_color=cor_texto, coloraxis_showscale=False,
            margin=dict(l=10,r=15,t=55,b=20), xaxis_title="", yaxis_title="",
            xaxis=dict(gridcolor=cor_grid)
        )
        fig_score.update_traces(textposition="outside")
        st.plotly_chart(fig_score, use_container_width=True)

    with g2:
        fig_market = px.scatter(
            df_filtrado, x="Preco_Atual", y="FPS_1080p", size="VRAM",
            color="Marca", hover_name="GPU", hover_data=["Loja", "Score"],
            template=plotly_template,
            color_discrete_sequence=["#6366f1","#06b6d4","#f59e0b"]
        )
        fig_market.update_layout(
            title="Preço × desempenho", height=390, paper_bgcolor=cor_card,
            plot_bgcolor=cor_card, font_color=cor_texto,
            margin=dict(l=15,r=15,t=55,b=20), xaxis_title="Preço atual (R$)",
            yaxis_title="FPS médio raster · 1080p Ultra", xaxis=dict(gridcolor=cor_grid),
            yaxis=dict(gridcolor=cor_grid), legend_title=""
        )
        st.plotly_chart(fig_market, use_container_width=True)

    st.markdown('<div class="section-title">Ranking detalhado</div>', unsafe_allow_html=True)
    tabela = df_filtrado.copy()
    tabela["Preço"] = tabela["Preco_Atual"].apply(formatar_moeda)
    tabela["VRAM"] = tabela["VRAM"].astype(int).astype(str) + " GB"
    tabela["Atualizado"] = pd.to_datetime(tabela["Data_Coleta"], errors="coerce", utc=True)
    st.dataframe(
        tabela[["#","GPU","Marca","Loja","Preço","VRAM","FPS_1080p","FPS_1440p",
                "FPS_RT_1080p","Score","Origem_Preco","Atualizado",
                "Fonte_Especificacoes","Link"]],
        column_config={
            "FPS_1080p": st.column_config.ProgressColumn("Raster 1080p Ultra",min_value=0,max_value=140,format="%.1f"),
            "FPS_1440p": st.column_config.ProgressColumn("Raster 1440p Ultra",min_value=0,max_value=100,format="%.1f"),
            "FPS_RT_1080p": st.column_config.NumberColumn("RT 1080p Ultra",format="%.1f"),
            "Score": st.column_config.NumberColumn("Score",format="%.1f"),
            "Origem_Preco": "Origem",
            "Atualizado": st.column_config.DatetimeColumn("Atualizado",format="DD/MM HH:mm"),
            "Fonte_Especificacoes": st.column_config.LinkColumn(
                "Ficha técnica", display_text="Abrir fonte ↗"
            ),
            "Link": st.column_config.LinkColumn("Oferta",display_text="Abrir loja ↗"),
        },
        hide_index=True, use_container_width=True, height=360
    )

with aba_comparador:
    st.markdown('<div class="section-title">Compare lado a lado</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Selecione até três GPUs para analisar os principais indicadores.</div>', unsafe_allow_html=True)
    opcoes = df_filtrado["GPU"].tolist()
    comparar = st.multiselect(
        "GPUs para comparar", opcoes, default=opcoes[:min(3,len(opcoes))], max_selections=3
    )
    if len(comparar) < 2:
        st.info("Selecione pelo menos duas GPUs.")
    else:
        df_comp = df_filtrado[df_filtrado["GPU"].isin(comparar)].copy()
        cards = st.columns(len(df_comp))
        for coluna, (_, row) in zip(cards, df_comp.iterrows()):
            with coluna:
                with st.container(border=True):
                    st.caption(f"{row['Marca']} · {row['Loja']}")
                    st.subheader(row["GPU"])
                    st.metric("Preço",formatar_moeda(row["Preco_Atual"]))
                    a,b = st.columns(2)
                    a.metric("Raster 1080p",f"{row['FPS_1080p']:.1f} FPS")
                    b.metric("Raster 1440p",f"{row['FPS_1440p']:.1f} FPS")
                    av1 = "AV1 encode" if row["AV1_Encode"] else "sem AV1 encode"
                    st.caption(
                        f"{int(row['VRAM'])} GB · {int(row['Consumo_W'])} W · "
                        f"{av1} · Índice {row['Score']:.1f}"
                    )

        categorias=["Raster 1080p","Raster 1440p","Ray tracing","Eficiência","VRAM"]
        max_1080 = df_base["FPS_1080p"].max()
        max_1440 = df_base["FPS_1440p"].max()
        max_rt = df_base["FPS_RT_1080p"].max()
        max_eficiencia = (df_base["FPS_1080p"] / df_base["Consumo_W"]).max()
        fig_radar=go.Figure()
        for _,row in df_comp.iterrows():
            valores=[
                row["FPS_1080p"] / max_1080 * 100,
                row["FPS_1440p"] / max_1440 * 100,
                row["FPS_RT_1080p"] / max_rt * 100,
                (row["FPS_1080p"] / row["Consumo_W"]) / max_eficiencia * 100,
                min(row["VRAM"] / 12 * 100, 100),
            ]
            fig_radar.add_trace(go.Scatterpolar(
                r=valores+[valores[0]],theta=categorias+[categorias[0]],
                fill="toself",name=row["GPU"],opacity=.7
            ))
        fig_radar.update_layout(
            title="Perfil comparativo normalizado",template=plotly_template,
            paper_bgcolor=cor_card,font_color=cor_texto,height=480,
            polar=dict(bgcolor=cor_card,radialaxis=dict(visible=True,range=[0,100],gridcolor=cor_grid),
                       angularaxis=dict(gridcolor=cor_grid)),
            margin=dict(l=40,r=40,t=70,b=40),legend=dict(orientation="h",y=-.12)
        )
        st.plotly_chart(fig_radar,use_container_width=True)

with aba_ofertas:
    st.markdown('<div class="section-title">Ofertas verificadas</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Loja e link mudam automaticamente quando surge uma opção válida mais barata.</div>',
        unsafe_allow_html=True
    )
    ofertas=df_filtrado.sort_values("Preco_Atual").reset_index(drop=True)
    for inicio in range(0,len(ofertas),3):
        colunas=st.columns(3)
        for coluna,(_,row) in zip(colunas,ofertas.iloc[inicio:inicio+3].iterrows()):
            with coluna:
                with st.container(border=True):
                    origem_texto="Oferta verificada" if row["Origem_Preco"]=="Automático" else "Valor de referência"
                    st.markdown(
                        f'<div class="offer-store">{row["Loja"]}</div>'
                        f'<div class="offer-name">{row["GPU"]}</div>'
                        f'<div class="offer-price">{formatar_moeda(row["Preco_Atual"])}</div>'
                        f'<div class="offer-meta">{origem_texto} · {int(row["VRAM"])} GB · '
                        f'{row["FPS_1080p"]:.1f} FPS raster médio*</div>',
                        unsafe_allow_html=True
                    )
                    st.link_button("Ver oferta na loja ↗",row["Link"],use_container_width=True)
    st.caption(
        "* Média 1080p Ultra da suíte referenciada. Preços, estoque, frete e "
        "pagamento podem mudar; confirme na loja antes da compra."
    )




