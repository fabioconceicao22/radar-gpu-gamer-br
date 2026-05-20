import os
import streamlit as st
import pandas as pd
import altair as alt

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Radar GPU Gamer BR",
    page_icon="🎮",
    layout="wide"
)

# ============================================================
# CSS DARK PREMIUM
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
}

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

[data-testid="stDataFrame"] {
    background-color: #111827;
    border-radius: 14px;
    border: 1px solid #334155;
    padding: 6px;
}

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
}

.hero-subtitle {
    font-size: 14px;
    color: #cbd5e1;
    margin-top: 4px;
}

.section-title {
    font-size: 22px;
    font-weight: 800;
    margin-top: 6px;
    margin-bottom: 4px;
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
        "VRAM": 8,
        "FPS_1080p": 112,
        "FPS_1440p": 72,
        "Streaming_Score": 72,
        "Gamer_Score": 91,
        "Consumo_W": 165,
        "Preco_Antigo": 1899.99
    },

    {
        "GPU": "Radeon RX 6600 8GB",
        "Modelo": "ASRock Challenger D",
        "Marca": "AMD",
        "VRAM": 8,
        "FPS_1080p": 88,
        "FPS_1440p": 52,
        "Streaming_Score": 64,
        "Gamer_Score": 84,
        "Consumo_W": 132,
        "Preco_Antigo": 1899.99
    },

    {
        "GPU": "GeForce RTX 4060 8GB",
        "Modelo": "Galax 1-Click OC",
        "Marca": "NVIDIA",
        "VRAM": 8,
        "FPS_1080p": 108,
        "FPS_1440p": 68,
        "Streaming_Score": 93,
        "Gamer_Score": 88,
        "Consumo_W": 115,
        "Preco_Antigo": 3999.99
    },

    {
        "GPU": "Intel Arc B580 12GB",
        "Modelo": "ASRock Challenger OC",
        "Marca": "Intel",
        "VRAM": 12,
        "FPS_1080p": 116,
        "FPS_1440p": 78,
        "Streaming_Score": 80,
        "Gamer_Score": 89,
        "Consumo_W": 190,
        "Preco_Antigo": 2299.99
    },

    {
        "GPU": "GeForce RTX 4070 SUPER 12GB",
        "Modelo": "Gigabyte Windforce OC",
        "Marca": "NVIDIA",
        "VRAM": 12,
        "FPS_1080p": 178,
        "FPS_1440p": 132,
        "Streaming_Score": 96,
        "Gamer_Score": 94,
        "Consumo_W": 220,
        "Preco_Antigo": 4899.99
    },

{
        "GPU": "GeForce RTX 5060 EPIC-X RGB OC 8GB",
        "Modelo": "EPIC-X RGB OC Triple Fan",
        "Marca": "NVIDIA",
        "VRAM": 12,
        "FPS_1080p": 178,
        "FPS_1440p": 132,
        "Streaming_Score": 96,
        "Gamer_Score": 94,
        "Consumo_W": 220,
        "Preco_Antigo": 4899.99
    },
    
    {
        "GPU": "GeForce RTX 3060 12GB",
        "Modelo": "Galax 1-Click OC",
        "Marca": "NVIDIA",
        "VRAM": 12,
        "FPS_1080p": 96,
        "FPS_1440p": 62,
        "Streaming_Score": 86,
        "Gamer_Score": 82,
        "Consumo_W": 170,
        "Preco_Antigo": 2399.99
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

    valor = str(valor).strip()

    valor = (
        valor
        .replace("R$", "")
        .replace(" ", "")
    )

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
        return "KaBuM!"

    if "amazon" in link or "amzn.to" in link:
        return "Amazon"

    if "mercadolivre" in link or "meli.la" in link:
        return "Mercado Livre"

    if "terabyte" in link:
        return "Terabyte"

    if "ebay" in link:
        return "eBay"
    
    if "aliexpress" in link:
        return "AliExpress"
    
    return "Loja não identificada"


def calcular_score(row, foco):
    preco = row["Preco_Atual"]

    if preco <= 0:
        return 0

    fps_1080p = row["FPS_1080p"]
    fps_1440p = row["FPS_1440p"]

    custo_fps = fps_1080p / preco
    eficiencia = fps_1080p / row["Consumo_W"]
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
        custo_fps_1440 = fps_1440p / preco

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


# ============================================================
# CARREGAR CSV AUTOMÁTICO
# ============================================================

@st.cache_data
def carregar_dados():

    caminho_csv = "data/precos_coletados.csv"

    if not os.path.exists(caminho_csv):
        st.error("Arquivo data/precos_coletados.csv não encontrado.")
        st.stop()

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

        "produto": "GPU",
        "gpu": "GPU",

        "site": "Loja",
        "loja": "Loja",

        "link": "Link",
        "url": "Link",

        "preco": "Preco_Atual",
        "preço": "Preco_Atual",
        "preco atual": "Preco_Atual",
        "preço atual": "Preco_Atual",

        "marca": "Marca",
        "modelo": "Modelo",

        "data_coleta": "Data_Coleta"
    })

    colunas_minimas = [
        "GPU",
        "Link",
        "Preco_Atual"
    ]

    for coluna in colunas_minimas:
        if coluna not in df_precos.columns:
            st.error(f"Coluna obrigatória ausente no CSV: {coluna}")
            st.write("Colunas encontradas:")
            st.write(df_precos.columns.tolist())
            st.stop()

    if "Loja" not in df_precos.columns:
        df_precos["Loja"] = df_precos["Link"].apply(identificar_loja)

    df_precos["Preco_Atual"] = df_precos["Preco_Atual"].apply(
        normalizar_preco
    )

    df_precos = df_precos.dropna(
        subset=["Preco_Atual"]
    )

    df_precos = df_precos[
        df_precos["Preco_Atual"] > 0
    ]

    if df_precos.empty:
        st.error("O CSV foi lido, mas todos os preços estão zerados ou inválidos.")
        st.write("Verifique o arquivo data/precos_coletados.csv")
        st.stop()

    df = pd.merge(
        df_precos,
        df_base,
        on="GPU",
        how="left"
    )

    df = df.dropna(
        subset=[
            "VRAM",
            "FPS_1080p",
            "FPS_1440p",
            "Streaming_Score",
            "Gamer_Score",
            "Consumo_W"
        ]
    )

    if df.empty:
        st.error("Nenhuma GPU do CSV bateu com a base técnica.")
        st.write("GPUs encontradas no CSV:")
        st.write(df_precos["GPU"].tolist())
        st.stop()

    return df


# ============================================================
# CARREGAMENTO
# ============================================================

df = carregar_dados()

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">🎮 Radar GPU Gamer BR</div>
        <div class="hero-subtitle">
            Dashboard gamer com coleta automática de preços.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# FILTROS
# ============================================================

with st.sidebar:

    st.title("⚙️ Filtros")

    marcas = ["Todas"] + sorted(
        df["Marca"].dropna().unique().tolist()
    )

    marca = st.selectbox(
        "Marca",
        marcas
    )

    foco = st.selectbox(
        "Foco da análise",
        [
            "Gamer 1080p",
            "Streamer",
            "Gamer 1440p"
        ]
    )

    preco_maximo = st.slider(
        "Preço máximo",
        min_value=1000,
        max_value=10000,
        value=10000,
        step=100
    )

# ============================================================
# PROCESSAMENTO
# ============================================================

df_filtrado = df.copy()

if marca != "Todas":
    df_filtrado = df_filtrado[
        df_filtrado["Marca"] == marca
    ]

df_filtrado = df_filtrado[
    df_filtrado["Preco_Atual"] <= preco_maximo
]

if df_filtrado.empty:
    st.warning(
        "Nenhuma GPU encontrada com os filtros atuais."
    )
    st.stop()

df_filtrado["Score"] = df_filtrado.apply(
    lambda row: calcular_score(row, foco),
    axis=1
)

df_filtrado["Desconto_%"] = (
    (
        (
            df_filtrado["Preco_Antigo"] -
            df_filtrado["Preco_Atual"]
        )
        /
        df_filtrado["Preco_Antigo"]
    ) * 100
).round(1)

df_filtrado["Custo_por_FPS"] = (
    df_filtrado["Preco_Atual"] /
    df_filtrado["FPS_1080p"]
).round(2)

df_filtrado = df_filtrado.sort_values(
    by="Score",
    ascending=False
)

# ============================================================
# INDICADORES
# ============================================================

melhor = df_filtrado.iloc[0]

menor_preco = df_filtrado.sort_values(
    by="Preco_Atual"
).iloc[0]

maior_desconto = df_filtrado.sort_values(
    by="Desconto_%",
    ascending=False
).iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "🏆 Melhor custo-benefício",
    melhor["GPU"],
    f'Score {melhor["Score"]}'
)

col2.metric(
    "💰 Menor preço",
    menor_preco["GPU"],
    formatar_moeda(menor_preco["Preco_Atual"])
)

col3.metric(
    "📉 Maior desconto",
    f'{maior_desconto["Desconto_%"]}%',
    maior_desconto["Loja"]
)

# ============================================================
# TABELA
# ============================================================

st.markdown(
    '<div class="section-title">🏁 Ranking de GPUs</div>',
    unsafe_allow_html=True
)

df_exibicao = df_filtrado.copy()

df_exibicao["Preço Atual"] = (
    df_exibicao["Preco_Atual"]
    .apply(formatar_moeda)
)

df_exibicao["Preço Antigo"] = (
    df_exibicao["Preco_Antigo"]
    .apply(formatar_moeda)
)

st.dataframe(

    df_exibicao[[
        "GPU",
        "Modelo",
        "Marca",
        "Loja",
        "Preço Atual",
        "Preço Antigo",
        "Desconto_%",
        "VRAM",
        "FPS_1080p",
        "FPS_1440p",
        "Custo_por_FPS",
        "Score"
    ]],

    use_container_width=True,
    hide_index=True,
    height=320
)

# ============================================================
# GRÁFICOS
# ============================================================

st.markdown(
    '<div class="section-title">📈 Comparativo</div>',
    unsafe_allow_html=True
)

grafico = alt.Chart(df_filtrado).mark_bar().encode(

    x=alt.X("GPU", sort="-y"),

    y="Score",

    tooltip=[
        "GPU",
        "Score",
        "Preco_Atual"
    ]

)

st.altair_chart(
    grafico,
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

    c1, c2, c3, c4 = st.columns([4, 1.2, 1.2, 1.2])

    with c1:
        st.markdown(
            f"""
            **{row['GPU']} - {row['Modelo']}**  
            {row['Loja']}
            """
        )

    with c2:
        st.markdown(
            f"""
            <div style="font-size:18px; font-weight:700; color:white; padding-top:8px;">
                {formatar_moeda(row['Preco_Atual'])}
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div style="font-size:16px; font-weight:700; color:white; padding-top:8px;">
                Score: {row['Score']}
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <a href="{row['Link']}" target="_blank" style="text-decoration:none;">
                <div style="
                    background: linear-gradient(135deg,#22c55e,#16a34a);
                    color: white;
                    padding: 11px 16px;
                    border-radius: 10px;
                    font-weight: 800;
                    text-align: center;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.35);
                ">
                    🛒 Comprar
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "<hr style='border:0.5px solid #1e293b; margin:12px 0;'>",
        unsafe_allow_html=True
    )
