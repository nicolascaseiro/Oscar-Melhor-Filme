import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard - Filmes do Oscar", layout="wide")

@st.cache_data
def carregar_dados():
    url = "https://raw.githubusercontent.com/nicolascaseiro/Oscar-Melhor-Filme/refs/heads/main/oscar_melhor_filme.csv"
    df = pd.read_csv(url)
    return df

df = carregar_dados()

# Sidebar - Filtros
st.sidebar.header("🎬 Filtros")

# Filtro: Venceu Melhor Filme
venceu_oscar = st.sidebar.selectbox(
    "Venceu Melhor Filme?",
    options=["Todos", "Sim", "Não"],
    index=0
)

# Aplicar filtro antes dos explode
df_base = df.copy()

if venceu_oscar == "Sim":
    df_base = df_base[df_base['venceu_melhor_filme'] == True]
elif venceu_oscar == "Não":
    df_base = df_base[df_base['venceu_melhor_filme'] == False]

# Adiciona colunas auxiliares e explode listas
df_base['década'] = (df_base['ano'] // 10 * 10).astype('Int64').astype(str) + 's'
df_base['diretores_lista'] = df_base['direção'].fillna('').apply(lambda x: [d.strip() for d in x.split(',') if d.strip()])
df_base = df_base.explode('diretores_lista')

df_base['atores_lista'] = df_base['elenco_principal'].fillna('').apply(lambda x: [a.strip() for a in x.split(',') if a.strip()])
df_base = df_base.explode('atores_lista')

df_base['gêneros_lista'] = df_base['gêneros'].fillna('').apply(lambda x: [g.strip() for g in x.split(',') if g.strip()])
df_base = df_base.explode('gêneros_lista')

# Sidebar - Filtros adicionais
decadas = sorted(df_base['década'].dropna().unique())
generos = sorted(df_base['gêneros_lista'].dropna().unique())
diretores = sorted(df_base['diretores_lista'].dropna().unique())
atores = sorted(df_base['atores_lista'].dropna().unique())

decada_selecionada = st.sidebar.multiselect("Década", decadas)
genero_selecionado = st.sidebar.multiselect("Gênero", generos)
diretor_selecionado = st.sidebar.multiselect("Diretor", diretores)
ator_selecionado = st.sidebar.multiselect("Ator/Atriz", atores)

# Aplicação dos filtros
df_filtrado = df_base.copy()

if decada_selecionada:
    df_filtrado = df_filtrado[df_filtrado['década'].isin(decada_selecionada)]
if genero_selecionado:
    df_filtrado = df_filtrado[df_filtrado['gêneros_lista'].isin(genero_selecionado)]
if diretor_selecionado:
    df_filtrado = df_filtrado[df_filtrado['diretores_lista'].isin(diretor_selecionado)]
if ator_selecionado:
    df_filtrado = df_filtrado[df_filtrado['atores_lista'].isin(ator_selecionado)]

df_filtrado_unico = df_filtrado.drop_duplicates(subset=['título', 'ano'])

# Título e Métricas
st.title("🏆 Dashboard dos Filmes do Oscar")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🎬 Total de Filmes", df_filtrado_unico.shape[0])
col2.metric("⭐ Nota Média do IMDb", f"{df_filtrado_unico['nota_imdb'].mean():.2f}")
col3.metric("🎞️ Nota Média do Letterboxd", f"{df_filtrado_unico['nota_letterboxd'].mean():.2f}")
col4.metric("🎥 Diretores Diferentes", df_filtrado_unico['diretores_lista'].nunique())
col5.metric("🏅 Total de Vitórias (todas categorias)", int(df_filtrado_unico['vitórias'].sum()))

st.markdown("---")

# Gráfico: Nota média por gênero
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

fig.update_traces(
    textposition='outside',
    marker_line_width=1.5,
    marker_line_color='black',
    textfont=dict(color='black')
)

fig.update_layout(
    plot_bgcolor='white',
    title_font=dict(size=22, family='Verdana', color='black'),
    xaxis_tickangle=-45,
    xaxis_title_font=dict(size=16, color='black'),
    yaxis_title_font=dict(size=16, color='black'),
    yaxis=dict(
        range=[0, df_grafico['nota_imdb'].max() + 1],
        tickfont=dict(color='black')
    ),
    margin=dict(l=40, r=40, t=100, b=100),
    font=dict(color='black'),
    xaxis=dict(tickfont=dict(color='black'))
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Tabela de filmes
colunas_exibir = [
    'título', 'ano', 'gêneros', 'direção',
    'nota_imdb', 'nota_letterboxd', 'indicações', 'vitórias', 'venceu_melhor_filme'
]

df_tabela_formatada = df_filtrado_unico[colunas_exibir].copy()
df_tabela_formatada['nota_letterboxd'] = df_tabela_formatada['nota_letterboxd'].map(lambda x: f"{x:.1f}" if pd.notnull(x) else "-")
df_tabela_formatada['nota_imdb'] = df_tabela_formatada['nota_imdb'].map(lambda x: f"{x:.1f}" if pd.notnull(x) else "-")

st.subheader("📋 Tabela de Filmes")
st.dataframe(df_tabela_formatada)
