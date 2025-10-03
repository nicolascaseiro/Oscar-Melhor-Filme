import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard - Filmes do Oscar", layout="wide")

@st.cache_data
def carregar_dados():
    url = "https://raw.githubusercontent.com/nicolascaseiro/Oscar-Melhor-Filme/refs/heads/main/oscar_melhor_filme.csv"
    df = pd.read_csv(url)
    return df

# Carregar dados
df = carregar_dados()

# Criar coluna de década
df['década'] = (df['ano'] // 10 * 10).astype('Int64').astype(str) + 's'

# Separar diretores em lista
df['diretores_lista'] = df['direção'].fillna('').apply(lambda x: [d.strip() for d in x.split(',') if d.strip() != ''])
df = df.explode('diretores_lista')

# Separar elenco principal em lista (atores)
df['atores_lista'] = df['elenco_principal'].fillna('').apply(lambda x: [a.strip() for a in x.split(',') if a.strip() != ''])
df = df.explode('atores_lista')

# Separar gêneros em lista
df['gêneros_lista'] = df['gêneros'].fillna('').apply(lambda x: [g.strip() for g in x.split(',') if g.strip() != ''])
df = df.explode('gêneros_lista')

# Sidebar de filtros
st.sidebar.header("🎬 Filtros")

decadas = sorted(df['década'].dropna().unique())
generos = sorted(df['gêneros_lista'].dropna().unique())
diretores = sorted(df['diretores_lista'].dropna().unique())
atores = sorted(df['atores_lista'].dropna().unique())

decada_selecionada = st.sidebar.multiselect("Década", decadas)
genero_selecionado = st.sidebar.multiselect("Gênero", generos)
diretor_selecionado = st.sidebar.multiselect("Diretor", diretores)
ator_selecionado = st.sidebar.multiselect("Ator/Atriz", atores)

# Aplicar filtros
df_filtrado = df.copy()

if decada_selecionada:
    df_filtrado = df_filtrado[df_filtrado['década'].isin(decada_selecionada)]

if genero_selecionado:
    df_filtrado = df_filtrado[df_filtrado['gêneros_lista'].isin(genero_selecionado)]

if diretor_selecionado:
    df_filtrado = df_filtrado[df_filtrado['diretores_lista'].isin(diretor_selecionado)]

if ator_selecionado:
    df_filtrado = df_filtrado[df_filtrado['atores_lista'].isin(ator_selecionado)]

# Remover duplicatas por título + ano para evitar remover filmes com mesmo nome
df_filtrado_unico = df_filtrado.drop_duplicates(subset=['título', 'ano'])

# Título e Métricas
st.title("🏆 Dashboard dos Filmes do Oscar")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🎬 Total de Filmes", df_filtrado_unico.shape[0])
col2.metric("⭐ Média IMDb", f"{df_filtrado_unico['nota_imdb'].mean():.2f}")
col3.metric("🎥 Diretores Únicos", df_filtrado_unico['diretores_lista'].nunique())
col4.metric("🏅 Total de Vitórias", int(df_filtrado_unico['vitórias'].sum()))

st.markdown("---")

# Gráfico de nota média por gênero
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

# Tabela final
colunas_exibir = [
    'título', 'ano', 'gêneros', 'direção',
    'nota_imdb', 'nota_letterboxd', 'indicações', 'vitórias', 'venceu_melhor_filme'
]
st.subheader("📋 Tabela de Filmes")
st.dataframe(df_filtrado_unico[colunas_exibir])
