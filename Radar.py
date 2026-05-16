import streamlit as st
import pandas as pd

# ============================================================
# Radar GPU Gamer BR
# Versão compacta + correção toolbar dos gráficos
# ============================================================

st.set_page_config(
    page_title="Radar GPU Gamer BR",
    page_icon="🎮",
    layout="wide"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #0f172a;
    color: #f8fafc;
}

.main .block-container {
    padding-top: 0.6rem;
    padding-bottom: 0.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 100%;
}

#MainMenu, footer, header {
    visibility: hidden;
}

h1, h2, h3, h4, h5, h6, p, span, label {
    color: #f8fafc !important;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1e293b;
}

/* Selectbox visível */
.stSelectbox div[data-baseweb="select"] {
    background-color: #ffffff !important;
    color: #111827 !important;
    border-radius: 10px;
}

.stSelectbox div[data-baseweb="select"] * {
    color: #111827 !important;
}

div[data-baseweb="popover"],
ul[role="listbox"] {
    background-color: #ffffff !important;
}

div[data-baseweb="popover"] *,
li[role="option"] {
    color: #111827 !important;
    background-color: #ffffff !important;
}

li[role="option"]:hover {
    background-color: #e5e7eb !important;
    color: #111827 !important;
}

/* Cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg,#111827,#172554);
    border: 1px solid #334155;
    padding: 10px 14px;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.40);
    min-height: 90px;
}

[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
    font-size: 13px !important;
}

[data-testid="stMetricValue"] {
    color: #22c55e !important;
    font-size: 20px !important;
}

[data-testid="stMetricDelta"] {
    font-size: 12px !important;
}

/* Tabela */
[data-testid="stDataFrame"] {
    background-color: #111827;
    border-radius: 14px;
    border: 1px solid #334155;
    padding: 6px;
}

/* Alertas */
.stAlert {
    border-radius: 12px;
    border: 1px solid #334155;
    padding: 8px !important;
}

/* Remove toolbar branca dos gráficos */
.vega-embed summary {
    display: none !important;
}

.vega-actions {
    display: none !important;
}

/* Links */
a {
    color: #38bdf8 !important;
}

/* Divisores */
hr {
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    border-color: #334155;
}

/* Títulos */
.section-title {
    font-size: 22px;
    font-weight: 800;
    margin-top: 6px;
    margin-bottom: 4px;
}

/* Hero */
.hero-box {
    background: linear-gradient(135deg,#111827,#1e3a8a);
    padding: 14px 18px;
    border-radius: 18px;
    border: 1px solid #334155;
    box-shadow: 0 6px 20px rgba(0,0,0,0.40);
    margin-bottom: 10px;
}

.hero-title {
    font-size: 30px;
    font-weight: 900;
    color: #f8fafc;
    line-height: 1.1;
}

.hero-subtitle {
    font-size: 14px;
    color: #cbd5e1;
    margin-top: 4px;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}

div[data-testid="stHorizontalBlock"] {
    gap: 0.8rem;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# DADOS
# ============================================================

gpus = [
    {
        "GPU": "Radeon RX 7600 8GB",
        "Modelo": "Sapphire Pulse",
        "Marca": "AMD",
        "Loja": "Kabum",
        "Preco Atual": 1699,
        "Preco Antigo": 1899,
        "VRAM": 8,
        "FPS 1080p": 112,
        "FPS 1440p": 72,
        "Streaming Score": 72,
        "Gamer Score": 91,
        "Consumo W": 165,
        "Link": "https://www.kabum.com.br"
    },
    {
        "GPU": "Radeon RX 6600 8GB",
        "Modelo": "ASRock Challenger D",
        "Marca": "AMD",
        "Loja": "Pichau",
        "Preco Atual": 1299,
        "Preco Antigo": 1499,
        "VRAM": 8,
        "FPS 1080p": 88,
        "FPS 1440p": 52,
        "Streaming Score": 64,
        "Gamer Score": 84,
        "Consumo W": 132,
        "Link": "https://www.pichau.com.br"
    },
    {
        "GPU": "GeForce RTX 4060 8GB",
        "Modelo": "MSI Ventus 2X OC",
        "Marca": "NVIDIA",
        "Loja": "Amazon",
        "Preco Atual": 1849,
        "Preco Antigo": 2099,
        "VRAM": 8,
        "FPS 1080p": 108,
        "FPS 1440p": 68,
        "Streaming Score": 93,
        "Gamer Score": 88,
        "Consumo W": 115,
        "Link": "https://www.amazon.com.br"
    },
    {
        "GPU": "Intel Arc B580 12GB",
        "Modelo": "Limited Edition",
        "Marca": "Intel",
        "Loja": "Terabyte",
        "Preco Atual": 1999,
        "Preco Antigo": 2199,
        "VRAM": 12,
        "FPS 1080p": 116,
        "FPS 1440p": 78,
        "Streaming Score": 80,
        "Gamer Score": 89,
        "Consumo W": 190,
        "Link": "https://www.terabyteshop.com.br"
    },
    {
        "GPU": "GeForce RTX 4070 SUPER 12GB",
        "Modelo": "ASUS Dual OC",
        "Marca": "NVIDIA",
        "Loja": "Mercado Livre",
        "Preco Atual": 3899,
        "Preco Antigo": 4299,
        "VRAM": 12,
        "FPS 1080p": 178,
        "FPS 1440p": 132,
        "Streaming Score": 96,
        "Gamer Score": 94,
        "Consumo W": 220,
        "Link": "https://www.mercadolivre.com.br"
    },
    {
        "GPU": "GeForce RTX 3060 12GB",
        "Modelo": "Galax 1-Click OC",
        "Marca": "NVIDIA",
        "Loja": "Magalu",
        "Preco Atual": 1799,
        "Preco Antigo": 1999,
        "VRAM": 12,
        "FPS 1080p": 96,
        "FPS 1440p": 62,
        "Streaming Score": 86,
        "Gamer Score": 82,
        "Consumo W": 170,
        "Link": "https://www.magazineluiza.com.br"
    }
]

df = pd.DataFrame(gpus)

# ============================================================
# FUNÇÃO DE SCORE
# ============================================================

def calcular_score(row, foco):
    preco = row["Preco Atual"]
    fps_1080p = row["FPS 1080p"]
    fps_1440p = row["FPS 1440p"]
    vram = row["VRAM"]
    streaming = row["Streaming Score"]
    gamer = row["Gamer Score"]
    consumo = row["Consumo W"]

    custo_fps = fps_1080p / preco
    eficiencia = fps_1080p / consumo
    vram_score = vram * 5

    if foco == "Streamer":
        score = (
            custo_fps * 1000 * 0.25 +
            streaming * 0.35 +
            gamer * 0.20 +
            vram_score * 0.10 +
            eficiencia * 50 * 0.10
        )

    elif foco == "Gamer 1440p":
        custo_fps_1440 = fps_1440p / preco

        score = (
            custo_fps_1440 * 1000 * 0.45 +
            gamer * 0.25 +
            vram_score * 0.15 +
            eficiencia * 50 * 0.15
        )

    else:
        score = (
            custo_fps * 1000 * 0.45 +
            gamer * 0.25 +
            vram_score * 0.10 +
            eficiencia * 50 * 0.20
        )

    return round(score, 2)

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero-box">
    <div class="hero-title">🎮 Radar GPU Gamer BR</div>
    <div class="hero-subtitle">
        Dashboard compacto para análise de GPUs gamer, streamer e custo-benefício.
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# FILTROS
# ============================================================

with st.sidebar:
    st.title("⚙️ Filtros")

    marca = st.selectbox(
        "Marca",
        ["Todas", "NVIDIA", "AMD", "Intel"]
    )

    foco = st.selectbox(
        "Foco da análise",
        ["Gamer 1080p", "Streamer", "Gamer 1440p"]
    )

    preco_maximo = st.slider(
        "Preço máximo",
        min_value=1000,
        max_value=5000,
        value=4500,
        step=100
    )

# ============================================================
# PROCESSAMENTO
# ============================================================

df_filtrado = df.copy()

if marca != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Marca"] == marca]

df_filtrado = df_filtrado[df_filtrado["Preco Atual"] <= preco_maximo]

df_filtrado["Score"] = df_filtrado.apply(
    lambda row: calcular_score(row, foco),
    axis=1
)

df_filtrado["Desconto %"] = (
    ((df_filtrado["Preco Antigo"] - df_filtrado["Preco Atual"]) / df_filtrado["Preco Antigo"]) * 100
).round(1)

df_filtrado["Custo por FPS"] = (
    df_filtrado["Preco Atual"] / df_filtrado["FPS 1080p"]
).round(2)

df_filtrado = df_filtrado.sort_values(by="Score", ascending=False)

# ============================================================
# INDICADORES
# ============================================================

if not df_filtrado.empty:
    melhor = df_filtrado.iloc[0]
    menor_preco = df_filtrado.sort_values(by="Preco Atual").iloc[0]
    maior_desconto = df_filtrado.sort_values(by="Desconto %", ascending=False).iloc[0]

    df_streamer = df.copy()
    df_streamer["Score"] = df_streamer.apply(
        lambda row: calcular_score(row, "Streamer"),
        axis=1
    )

    melhor_streamer = df_streamer.sort_values(
        by="Score",
        ascending=False
    ).iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🏆 Custo-benefício",
        melhor["GPU"],
        f'Score {melhor["Score"]}'
    )

    col2.metric(
        "💰 Menor preço",
        menor_preco["GPU"],
        f'R$ {menor_preco["Preco Atual"]}'
    )

    col3.metric(
        "📡 Streamer",
        melhor_streamer["GPU"],
        f'Score {melhor_streamer["Score"]}'
    )

    col4.metric(
        "📉 Maior desconto",
        f'{maior_desconto["Desconto %"]}%',
        maior_desconto["Loja"]
    )

else:
    st.warning("Nenhuma GPU encontrada com os filtros selecionados.")

# ============================================================
# INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">📊 Insights rápidos</div>',
    unsafe_allow_html=True
)

i1, i2, i3 = st.columns(3)

with i1:
    st.success(
        f"Recomendada: {melhor['GPU']} - {melhor['Modelo']}"
    )

with i2:
    st.info(
        f"Menor preço: R$ {menor_preco['Preco Atual']} na {menor_preco['Loja']}"
    )

with i3:
    st.warning(
        f"Foco: {foco}"
    )

# ============================================================
# RANKING
# ============================================================

st.markdown(
    '<div class="section-title">🏁 Ranking profissional de GPUs</div>',
    unsafe_allow_html=True
)

colunas = [
    "GPU",
    "Modelo",
    "Marca",
    "Loja",
    "Preco Atual",
    "Desconto %",
    "VRAM",
    "FPS 1080p",
    "FPS 1440p",
    "Custo por FPS",
    "Score"
]

st.dataframe(
    df_filtrado[colunas],
    use_container_width=True,
    hide_index=True,
    height=260
)

# ============================================================
# GRÁFICOS
# ============================================================

st.markdown(
    '<div class="section-title">📈 Comparações</div>',
    unsafe_allow_html=True
)

g1, g2 = st.columns(2)

with g1:
    st.write("### Score por GPU")
    st.bar_chart(
        df_filtrado.set_index("GPU")["Score"],
        height=220,
        use_container_width=True
    )

with g2:
    st.write("### Preço atual")
    st.bar_chart(
        df_filtrado.set_index("GPU")["Preco Atual"],
        height=220,
        use_container_width=True
    )

# ============================================================
# LINKS DE COMPRA
# ============================================================

st.markdown(
    '<div class="section-title">🛒 Links de compra</div>',
    unsafe_allow_html=True
)

for _, row in df_filtrado.iterrows():
    c1, c2, c3, c4 = st.columns([4, 1, 1, 1])

    c1.markdown(
        f"**{row['GPU']} - {row['Modelo']}**  \n"
        f"{row['Loja']}"
    )

    c2.markdown(f"**R$ {row['Preco Atual']}**")
    c3.markdown(f"Score: **{row['Score']}**")

    c4.markdown(
        f"""
        <a href="{row['Link']}" target="_blank">
            <button style="
                background: linear-gradient(135deg,#22c55e,#16a34a);
                color: white;
                border: none;
                padding: 8px 14px;
                border-radius: 10px;
                font-weight: bold;
                cursor: pointer;
                width: 100%;
                box-shadow: 0 4px 12px rgba(0,0,0,0.35);
            ">
                🛒 Comprar
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )
