import os
import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Radar GPU Gamer BR",
    page_icon="🎮",
    layout="wide"
)

# ============================================================
# CSS PREMIUM
# ============================================================

st.markdown("""
<style>

.stApp {
    background: #020817;
    color: #f8fafc;
}

.main .block-container {
    padding-top: 0.4rem;
    padding-bottom: 0.5rem;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
    max-width: 100%;
}

#MainMenu, footer, header {
    visibility: hidden;
}

h1, h2, h3, h4, h5, h6, p, span, label {
    color: #f8fafc !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#020817,#0f172a);
    border-right: 1px solid #1e293b;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #f8fafc !important;
    color: #020817 !important;
    border-radius: 10px;
}

.stSelectbox div[data-baseweb="select"] * {
    color: #020817 !important;
}

.hero-box {
    background: linear-gradient(135deg,#081226,#1e3a8a);
    padding: 18px 22px;
    border-radius: 18px;
    border: 1px solid #334155;
    box-shadow: 0 8px 28px rgba(0,0,0,0.45);
    margin-bottom: 12px;
}

.hero-title {
    font-size: 32px;
    font-weight: 900;
    letter-spacing: -0.5px;
}

.hero-subtitle {
    font-size: 14px;
    color: #cbd5e1;
    margin-top: 4px;
}

.kpi-card {
    background: linear-gradient(135deg,#081226,#111c44);
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 14px 16px;
    min-height: 105px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.35);
}

.kpi-title {
    color: #cbd5e1;
    font-size: 13px;
    font-weight: 700;
}

.kpi-value {
    color: #ffffff;
    font-size: 24px;
    font-weight: 900;
    margin-top: 6px;
}

.kpi-sub {
    color: #22c55e;
    font-size: 13px;
    font-weight: 800;
    margin-top: 6px;
}

.section-title {
    font-size: 22px;
    font-weight: 900;
    margin-top: 14px;
    margin-bottom: 8px;
}

[data-testid="stDataFrame"] {
    background-color: #081226;
    border-radius: 14px;
    border: 1px solid #334155;
    padding: 5px;
}

.chart-card {
    background: #081226;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 8px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.30);
}

.link-row {
    background: linear-gradient(135deg,#081226,#0f172a);
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 12px 14px;
    margin-bottom: 8px;
}

.buy-btn {
    background: linear-gradient(135deg,#22c55e,#16a34a);
    color: white !important;
    padding: 10px 16px;
    border-radius: 10px;
    font-weight: 900;
    text-align: center;
    box-shadow: 0 5px 14px rgba(22,163,74,0.35);
    text-decoration: none;
}

.small-muted {
    color: #94a3b8;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# BASE TÉCNICA DAS GPUS
# ============================================================

base_tecnica = [
    {
        "GPU": "Radeon RX 7600 8GB",
        "Modelo": "Sapphire Pulse OC",
        "Marca": "AMD",
        "Loja": "Pichau",
        "Preco_Atual": 1679.99,
        "Preco_Antigo": 1899.99,
        "VRAM": 8,
        "FPS_1080p": 112,
        "FPS_1440p": 72,
        "Streaming_Score": 72,
        "Gamer_Score": 91,
        "Consumo_W": 165,
        "Link": "https://www.pichau.com.br/"
    },
    {
        "GPU": "Radeon RX 6600 8GB",
        "Modelo": "ASRock Challenger D",
        "Marca": "AMD",
        "Loja": "KaBuM",
        "Preco_Atual": 1599.90,
        "Preco_Antigo": 1899.99,
        "VRAM": 8,
        "FPS_1080p": 88,
        "FPS_1440p": 52,
        "Streaming_Score": 64,
        "Gamer_Score": 84,
        "Consumo_W": 132,
        "Link": "https://www.kabum.com.br/"
    },
    {
        "GPU": "GeForce RTX 4060 8GB",
        "Modelo": "Galax 1-Click OC",
        "Marca": "NVIDIA",
        "Loja": "Amazon",
        "Preco_Atual": 3399.99,
        "Preco_Antigo": 3999.99,
        "VRAM": 8,
        "FPS_1080p": 108,
        "FPS_1440p": 68,
        "Streaming_Score": 93,
        "Gamer_Score": 88,
        "Consumo_W": 115,
        "Link": "https://www.amazon.com.br/"
    },
    {
        "GPU": "Intel Arc B580 12GB",
        "Modelo": "ASRock Challenger OC",
        "Marca": "Intel",
        "Loja": "KaBuM",
        "Preco_Atual": 1975.79,
        "Preco_Antigo": 2299.99,
        "VRAM": 12,
        "FPS_1080p": 116,
        "FPS_1440p": 78,
        "Streaming_Score": 80,
        "Gamer_Score": 89,
        "Consumo_W": 190,
        "Link": "https://www.kabum.com.br/"
    },
    {
        "GPU": "GeForce RTX 4070 SUPER 12GB",
        "Modelo": "Gigabyte Windforce OC",
        "Marca": "NVIDIA",
        "Loja": "Pichau",
        "Preco_Atual": 4602.19,
        "Preco_Antigo": 4899.99,
        "VRAM": 12,
        "FPS_1080p": 178,
        "FPS_1440p": 132,
        "Streaming_Score": 96,
        "Gamer_Score": 94,
        "Consumo_W": 220,
        "Link": "https://www.pichau.com.br/"
    },
    {
        "GPU": "GeForce RTX 5060 EPIC-X RGB OC 8GB",
        "Modelo": "EPIC-X RGB OC Triple Fan",
        "Marca": "NVIDIA",
        "Loja": "Pichau",
        "Preco_Atual": 2899.99,
        "Preco_Antigo": 3299.99,
        "VRAM": 8,
        "FPS_1080p": 130,
        "FPS_1440p": 82,
        "Streaming_Score": 95,
        "Gamer_Score": 90,
        "Consumo_W": 145,
        "Link": "https://www.pichau.com.br/"
    },
    {
        "GPU": "GeForce RTX 3060 12GB",
        "Modelo": "Galax 1-Click OC",
        "Marca": "NVIDIA",
        "Loja": "Amazon",
        "Preco_Atual": 1857.72,
        "Preco_Antigo": 2399.99,
        "VRAM": 12,
        "FPS_1080p": 96,
        "FPS_1440p": 62,
        "Streaming_Score": 86,
        "Gamer_Score": 82,
        "Consumo_W": 170,
        "Link": "https://www.amazon.com.br/"
    }
]

df_base = pd.DataFrame(base_tecnica)

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
        return "GeForce RTX 5060 EPIC-X RGB OC 8GB"
    if "3060" in texto:
        return "GeForce RTX 3060 12GB"
    if "b580" in texto or "arc" in texto:
        return "Intel Arc B580 12GB"

    return produto


def calcular_score(row, foco):
    preco = row["Preco_Atual"]

    if preco <= 0:
        return 0

    custo_fps = row["FPS_1080p"] / preco
    eficiencia = row["FPS_1080p"] / row["Consumo_W"]
    vram_score = row["VRAM"] * 5

    if foco == "Streamer":
        score = (
            custo_fps * 1000 * 0.25 +
            row["Streaming_Score"] * 0.35 +
            row["Gamer_Score"] * 0.20 +
            vram_score * 0.10 +
            eficiencia * 50 * 0.10
        )
    elif foco == "Gamer 1440p":
        custo_fps_1440 = row["FPS_1440p"] / preco
        score = (
            custo_fps_1440 * 1000 * 0.45 +
            row["Gamer_Score"] * 0.25 +
            vram_score * 0.15 +
            eficiencia * 50 * 0.15
        )
    else:
        score = (
            custo_fps * 1000 * 0.45 +
            row["Gamer_Score"] * 0.25 +
            vram_score * 0.10 +
            eficiencia * 50 * 0.20
        )

    return round(score, 2)


@st.cache_data
def carregar_dados():
    caminho_csv = "data/precos_coletados.csv"

    df = df_base.copy()
    df["Origem_Preco"] = "Base fixa"

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
            "Preco_Coletado"
        ]].rename(columns={
            "loja": "Loja_Auto",
            "link": "Link_Auto"
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

        colunas = df_base.columns.tolist() + ["Origem_Preco"]
        return df[colunas]

    except Exception:
        return df


df = carregar_dados()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## ⚙️ Filtros")

    marcas = ["Todas"] + sorted(df["Marca"].dropna().unique().tolist())

    marca = st.selectbox("Marca", marcas)

    foco = st.selectbox(
        "Foco da análise",
        ["Gamer 1080p", "Streamer", "Gamer 1440p"]
    )

    preco_maximo = st.slider(
        "Preço máximo",
        min_value=1000,
        max_value=10000,
        value=6000,
        step=100
    )

    st.markdown("---")
    st.markdown("### 🧩 Sobre o projeto")
    st.markdown(
        """
        O Radar GPU Gamer BR compara placas de vídeo por preço, desempenho e custo-benefício.

        Dados atualizados via CSV com fallback para base fixa.
        """
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("**Versão 2.0.0**")
    st.markdown("Desenvolvido com ❤️ por Fabio")

# ============================================================
# PROCESSAMENTO
# ============================================================

df_filtrado = df.copy()

if marca != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Marca"] == marca]

df_filtrado = df_filtrado[df_filtrado["Preco_Atual"] <= preco_maximo]

if df_filtrado.empty:
    st.warning("Nenhuma GPU encontrada com os filtros atuais.")
    st.stop()

df_filtrado["Score"] = df_filtrado.apply(
    lambda row: calcular_score(row, foco),
    axis=1
)

df_filtrado["Desconto_%"] = (
    (
        (df_filtrado["Preco_Antigo"] - df_filtrado["Preco_Atual"])
        / df_filtrado["Preco_Antigo"]
    ) * 100
).round(1)

df_filtrado["Custo_por_FPS"] = (
    df_filtrado["Preco_Atual"] / df_filtrado["FPS_1080p"]
).round(2)

df_filtrado = df_filtrado.sort_values(
    by="Score",
    ascending=False
).reset_index(drop=True)

df_filtrado["#"] = df_filtrado.index + 1

# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero-box">
    <div class="hero-title">🎮 Radar GPU Gamer BR</div>
    <div class="hero-subtitle">
        Análise, comparação e ranking das melhores placas de vídeo.
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# KPI CARDS
# ============================================================

melhor = df_filtrado.iloc[0]
menor_preco = df_filtrado.sort_values(by="Preco_Atual").iloc[0]
maior_desconto = df_filtrado.sort_values(by="Desconto_%", ascending=False).iloc[0]
fps_medio = int(df_filtrado["FPS_1080p"].mean())

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🖥️ GPUs analisadas</div>
        <div class="kpi-value">{len(df_filtrado)}</div>
        <div class="kpi-sub">Placas de vídeo</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🏷️ Menor preço</div>
        <div class="kpi-value">{formatar_moeda(menor_preco["Preco_Atual"])}</div>
        <div class="kpi-sub">{menor_preco["GPU"]}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🏆 Melhor score</div>
        <div class="kpi-value">{melhor["Score"]}</div>
        <div class="kpi-sub">{melhor["GPU"]}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📈 Média FPS 1080p</div>
        <div class="kpi-value">{fps_medio}</div>
        <div class="kpi-sub">Quadros por segundo</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# RANKING
# ============================================================

st.markdown(
    '<div class="section-title">🏁 Ranking de GPUs</div>',
    unsafe_allow_html=True
)

df_exibicao = df_filtrado.copy()

df_exibicao["Preço Atual"] = df_exibicao["Preco_Atual"].apply(formatar_moeda)
df_exibicao["Preço Antigo"] = df_exibicao["Preco_Antigo"].apply(formatar_moeda)
df_exibicao["Desconto"] = df_exibicao["Desconto_%"].astype(str) + "%"
df_exibicao["VRAM"] = df_exibicao["VRAM"].astype(str) + " GB"

st.dataframe(
    df_exibicao[[
        "#",
        "GPU",
        "Modelo",
        "Marca",
        "Loja",
        "Preço Atual",
        "Preço Antigo",
        "Desconto",
        "VRAM",
        "FPS_1080p",
        "FPS_1440p",
        "Custo_por_FPS",
        "Score",
        "Origem_Preco"
    ]],
    use_container_width=True,
    hide_index=True,
    height=300
)

# ============================================================
# COMPARATIVOS
# ============================================================

st.markdown(
    '<div class="section-title">📊 Comparativos</div>',
    unsafe_allow_html=True
)

g1, g2, g3, g4 = st.columns(4)

def grafico_barra(df_plot, y, titulo):
    fig = px.bar(
        df_plot,
        x="GPU",
        y=y,
        template="plotly_dark"
    )

    fig.update_traces(
        marker_color="#2563eb"
    )

    fig.update_layout(
        title=titulo,
        height=230,
        paper_bgcolor="#081226",
        plot_bgcolor="#081226",
        font_color="white",
        margin=dict(l=10, r=10, t=38, b=10),
        xaxis_title="",
        yaxis_title="",
        showlegend=False
    )

    fig.update_xaxes(
        tickangle=-90,
        tickfont=dict(size=9)
    )

    fig.update_yaxes(
        gridcolor="#1e293b"
    )

    return fig

with g1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(
        grafico_barra(df_filtrado, "Score", "Score por GPU"),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with g2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(
        grafico_barra(df_filtrado, "FPS_1080p", "FPS 1080p"),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with g3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(
        grafico_barra(df_filtrado, "FPS_1440p", "FPS 1440p"),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with g4:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(
        grafico_barra(df_filtrado, "Custo_por_FPS", "Custo por FPS"),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# LINKS DE COMPRA
# ============================================================

st.markdown(
    '<div class="section-title">🛒 Links de compra</div>',
    unsafe_allow_html=True
)

for _, row in df_filtrado.iterrows():

    c1, c2, c3, c4 = st.columns([4, 1.5, 1.2, 1.2])

    with c1:
        st.markdown(f"""
        <div class="link-row">
            <b>{row['GPU']} - {row['Modelo']}</b><br>
            <span class="small-muted">{row['Loja']} | {row['Origem_Preco']}</span>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style="font-size:17px; font-weight:900; padding-top:16px;">
            {formatar_moeda(row['Preco_Atual'])}
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div style="font-size:17px; font-weight:900; padding-top:16px;">
            {row['Score']}
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <a href="{row['Link']}" target="_blank" style="text-decoration:none;">
            <div class="buy-btn">🛒 Comprar</div>
        </a>
        """, unsafe_allow_html=True)
