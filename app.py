
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard - Filmes do Oscar", layout="wide")

# === Carregar dados ===
@st.cache_data
def carregar_dados():
    url = "https://raw.githubusercontent.com/nicolascaseiro/Oscar-Melhor-Filme/refs/heads/main/oscar_melhor_filme.csv"
    df = pd.read_csv(url)
    return df

df = carregar_dados()

# === Pré-processamento ===
df['gêneros_lista'] = df['gêneros'].fillna('').apply(lambda x: [g.strip() for g in x.split(',') if g.strip() != ''])
df = df.explode('gêneros_lista')

# === Sidebar ===
st.sidebar.header("🎬 Filtros")

anos = sorted(df['ano'].dropna().unique())
generos = sorted(df['gêneros_lista'].dropna().unique())
diretores = sorted(df['diretor'].dropna().unique())

ano_selecionado = st.sidebar.multiselect("Ano", anos)
genero_selecionado = st.sidebar.multiselect("Gênero", generos)
diretor_selecionado = st.sidebar.multiselect("Diretor", diretores)

df_filtrado = df.copy()

if ano_selecionado:
    df_filtrado = df_filtrado[df_filtrado['ano'].isin(ano_selecionado)]

if genero_selecionado:
    df_filtrado = df_filtrado[df_filtrado['gêneros_lista'].isin(genero_selecionado)]

if diretor_selecionado:
    df_filtrado = df_filtrado[df_filtrado['diretor'].isin(diretor_selecionado)]

# === KPIs ===
st.title("🏆 Dashboard dos Filmes do Oscar")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🎬 Total de Filmes", df_filtrado['título'].nunique())
col2.metric("⭐ Média IMDb", f"{df_filtrado['nota_imdb'].mean():.2f}")
col3.metric("🎥 Diretores Únicos", df_filtrado['diretor'].nunique())
col4.metric("🏅 Total de Vitórias", int(df_filtrado['vitórias'].sum()))

st.markdown("---")

# === Gráfico: Popularidade por Gênero ===
df_grafico = df_filtrado.groupby('gêneros_lista')['nota_imdb'].mean().reset_index()

fig = px.bar(
    df_grafico,
    x='gêneros_lista',
    y='nota_imdb',
    title='Nota Média IMDb por Gênero',
    labels={'gêneros_lista': 'Gênero', 'nota_imdb': 'Nota Média'},
    color='nota_imdb',
    color_continuous_scale='Viridis',
    text=df_grafico['nota_imdb'].round(2)
)

fig.update_traces(textposition='outside', marker_line_width=1.5, marker_line_color='black')
fig.update_layout(
    plot_bgcolor='white',
    title_font=dict(size=22, family='Verdana'),
    xaxis_tickangle=-45,
    xaxis_title_font=dict(size=16),
    yaxis_title_font=dict(size=16),
    margin=dict(l=40, r=40, t=80, b=100)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# === Tabela Final ===
colunas_exibir = ['título', 'ano', 'gêneros', 'diretor', 'nota_imdb', 'nota_letterboxd', 'indicações', 'vitórias', 'venceu_melhor_filme']
st.subheader("📋 Tabela de Filmes")
st.dataframe(df_filtrado[colunas_exibir])
