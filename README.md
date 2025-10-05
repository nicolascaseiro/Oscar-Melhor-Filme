# Oscar-Melhor-Filme
Análise de dados da lista de indicados ao Oscar de Melhor Filme.

🎯 [Dashboard](https://oscar-melhor-filme.streamlit.app/)

---

## 🆔 Identificação do Sistema

**Nome:** Dashboard dos Filmes do Oscar  
**Tecnologia:** Python + Streamlit  
**Fonte de dados:** Arquivo `.csv` hospedado no GitHub  
**Plataforma:** Web (via navegador)

---

## 📎 Diagrama de Caso de Uso

O diagrama abaixo representa os principais atores e funcionalidades do sistema de análise dos filmes indicados ao Oscar de Melhor Filme.

![Diagrama de Caso de Uso](caso-de-uso.png)

---

## 📌 Requisitos Funcionais

RF01 - O sistema deve carregar os dados dos filmes a partir de um arquivo .csv hospedado em uma URL pública no GitHub.  
RF02 - O sistema deve exibir filtros laterais para que o usuário possa selecionar um ou vários valores para visualizar diferentes subconjuntos de filmes, incluindo: status de vitória (Todos, Vencedores de Melhor Filme, Indicados não vencedores), com "Todos" selecionado por padrão no décadas, gêneros cinematográficos, diretores e atores/atrizes.  
RF03 - O sistema deve filtrar e atualizar dinamicamente os dados exibidos conforme os filtros aplicados pelo usuário.  
RF04 - O sistema deve permitir que os dados sejam exibidos mesmo sem nenhum filtro aplicado, mostrando a visualização completa.  
RF05 - O sistema deve exibir, no topo da tela, métricas agregadas dos dados filtrados ou não, incluindo: Total de filmes, Nota média do IMDb, Nota média do Letterboxd, Número de diretores distintos, Total de vitórias em todas as categorias.  
RF06 - O sistema deve gerar e exibir um gráfico de barras com a média de notas do IMDb por gênero, baseado no conjunto de dados filtrado.  
RF07 - O sistema deve apresentar uma tabela com os filmes filtrados ou não, contendo as seguintes colunas: Título, Ano, Gêneros, Direção, Nota IMDb, Nota Letterboxd, Indicações, Vitórias, Status de vencedor de Melhor Filme.  
RF08 - O sistema deve permitir que o usuário ordene a tabela de filmes por qualquer métrica exibida, em ordem crescente ou decrescente.

---

## 🛠️ Requisitos Não Funcionais

RNF01 – O sistema deve carregar e exibir os dados de forma ágil, proporcionando uma experiência fluida ao usuário durante a interação com filtros e gráficos, considerando as limitações da plataforma.  
RNF02 – A interface deve ser intuitiva e organizada, permitindo que usuários apliquem os filtros e visualizem as informações de maneira simples, sem necessidade de treinamento prévio.  
RNF03 – O sistema deve tratar adequadamente dados ausentes na tabela, prevenindo falhas durante a execução.  
RNF04 – Os dados exibidos são atualizados somente pelo mantenedor do repositório remoto, sem possibilidade de atualização pelo usuário final, garantindo controle centralizado das informações apresentadas.  
RNF05 – O sistema deve suportar o aumento gradual do volume de dados esperado para o domínio (considerando o número limitado de filmes indicados por ano), mantendo a responsividade e a capacidade de filtragem eficiente.  
RNF06 – O sistema deve ser acessível via navegador web em diferentes dispositivos, incluindo desktops e dispositivos móveis, sem necessidade de instalação ou cadastro do usuário.  
RNF07 – A comunicação para carregamento dos dados e acesso ao sistema é feita via protocolo seguro (HTTPS), garantindo a integridade e segurança da transmissão.  
RNF08 – O sistema deve utilizar mecanismos de cache para otimizar o desempenho, evitando recargas desnecessárias dos dados durante a mesma sessão.
