import pandas as pd
import streamlit as st
import statistics
import scipy.stats as scs
import plotly.express as px

from sqlalchemy import create_engine

# --- Streamlit Config ---

# Config page in widescreen
st.set_page_config(layout='wide')

#  without index column
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)

# --- Import Data from DataBase ---

def import_data():
    db = create_engine('sqlite:///scraping.sqlite', echo=False)
    conn = db.connect()
    query = """
        SELECT * FROM scraping;
    """
    data = pd.read_sql_query(query, con=conn)
    data['fit'] = data['fit'].apply(lambda x: x.replace('_fit', ''))
    return data

# --- Graphic Function ---

def scatter_plot(store, x, y):
    if x == 'Estilo':
        x = 'fit'
    elif x == 'Composição':
        x = 'composition'
    elif x == 'Preço':
        x = 'price'

    if y == 'Estilo':
        y = 'fit'
    elif y == 'Composição':
        y = 'composition'
    elif y == 'Preço':
        y = 'price'

    df_plotly = import_data()
    
    if store == 'Todas':
        df_plotly = df_plotly[[x, y]]
    elif store == 'H&M':
        df_plotly = df_plotly[df_plotly['store'] == 'hm'][[x, y]]
    elif store == 'Macys':
        df_plotly = df_plotly[df_plotly['store'] == 'macys'][[x, y]]

    if x == 'composition':
        w = 1200
        h = 700
        l = 0
        r = 0
    else:
        w = 1000
        h = 450
        l = 100
        r = 100

    fig = px.scatter(df_plotly, x=x, y=y, color=x, width=w, height=h)
    fig.update_layout(paper_bgcolor = None, 
                      plot_bgcolor = 'LightGrey',
                      margin=dict(l=l, r=r, t=0, b=0))
    return fig

# --- Page ---

def head():
    st.markdown("<h1 style='text-align: center; '>Projeto 'Webscraping' - Gustavo Michelsen</h1>", unsafe_allow_html=True)

def obj_prog():
    st.markdown("<h2 style='text-align: center; '>Objetivo do Projeto</h1>", unsafe_allow_html=True)
    with st.expander("", expanded=False):
        st.markdown("<h4 style='text-align: center; '>Plano de Fundo</h1>", unsafe_allow_html=True)
        st.write("O tema base do projeto é auxiliar investidores que pretendem abrir uma loja virtual, inicialmente focada em calças jeans masculina no mercado americano, mas que não tem nenhuma experiência no ramo. \n Como objetivo inicial, os investidores precisam saber diversas informações sobre os produtos, como preço de venda, cores e composição. \n Para coleta dos dados requeridos escolhi duas grandes lojas do mercado de moda, atuantes no mercado americano. São elas H&M e Macys.")
        st.markdown("<h4 style='text-align: center; '>Objetivo</h1>", unsafe_allow_html=True)
        st.write("Coletar dados relevantes sobre as calças jeans masculinas de duas grandes lojas americanas do ramo de moda - H&M e Macys.")
        st.write("Para mais informações sobre o projeto, acesse meu [portifólio](https://gustavomichelsen.github.io/portifolio_projetos/web_scraping.html).")

def data_desc():
    st.markdown("<h2 style='text-align: center; '>Descrição dos dados</h1>", unsafe_allow_html=True)
    with st.expander("Dados Gerais"):
        st.markdown("<h4 style='text-align: center; '>Coleta dos dados</h1>", unsafe_allow_html=True)
        st.write("A coleta dos dados ocorreu entre 20/08/2022 à 17/09/2022.")
        st.markdown("<h4 style='text-align: center; '>Total de dados obtidos</h1>", unsafe_allow_html=True)
        st.write("537")
        st.write("Nos dados coletados foram sendo acrescentados apenas itens novos, sendo a maior parte dos dados preenchidas no dia 20/08/2022.")

    df_clean = import_data()

    df_final = pd.DataFrame({'Loja' : ['H&M', 'Macys', 'Geral'], 
                            'Menor Preço' : [df_clean[df_clean['store'] == 'hm']['price'].min(), 
                                            df_clean[df_clean['store'] == 'macys']['price'].min(), 
                                            df_clean['price'].min()],

                            'Maior Preço' : [df_clean[df_clean['store'] == 'hm']['price'].max(), 
                                            df_clean[df_clean['store'] == 'macys']['price'].max(), 
                                            df_clean['price'].max()],

                            'Intervalo de Preços' : [df_clean[df_clean['store'] == 'hm']['price'].max() - df_clean[df_clean['store'] == 'hm']['price'].min(), 
                                                    df_clean[df_clean['store'] == 'macys']['price'].max() - df_clean[df_clean['store'] == 'macys']['price'].min(), 
                                                    df_clean['price'].max() - df_clean['price'].min()],

                            'Média de Preços' : [df_clean[df_clean['store'] == 'hm']['price'].mean(), 
                                                df_clean[df_clean['store'] == 'macys']['price'].mean(), 
                                                df_clean['price'].mean()],

                            'Mediana de Preços' : [df_clean[df_clean['store'] == 'hm']['price'].median(), 
                                                    df_clean[df_clean['store'] == 'macys']['price'].median(), 
                                                    df_clean['price'].median()],

                            'Desvio Padrão' : [statistics.stdev(df_clean[df_clean['store'] == 'hm']['price']),
                                                statistics.stdev(df_clean[df_clean['store'] == 'macys']['price']),
                                                statistics.stdev(df_clean['price'])],

                            'Skewness' : [scs.skew(df_clean[df_clean['store'] == 'hm']['price'], axis=0, bias=True),
                                        scs.skew(df_clean[df_clean['store'] == 'macys']['price'], axis=0, bias=True),
                                        scs.skew(df_clean['price'], axis=0, bias=True)],

                            'Kurtosis' : [scs.kurtosis(df_clean[df_clean['store'] == 'hm']['price'], axis=0, bias=True),
                                        scs.kurtosis(df_clean[df_clean['store'] == 'macys']['price'], axis=0, bias=True),
                                        scs.kurtosis(df_clean['price'], axis=0, bias=True)]})

    st.table(df_final)

    with st.expander("Ajuda sobre as métricas dos dados"):
        st.markdown("<h5 style='text-align: rigth; color:khaki '>Menor Preço</h1>", unsafe_allow_html=True)
        st.write("É o menor preço no conjunto de dados.")
        st.markdown("<h5 style='text-align: rigth; color:khaki '>Maior Preço</h1>", unsafe_allow_html=True)
        st.write("É o maior preço no conjunto de dados.")
        st.markdown("<h5 style='text-align: rigth; color:khaki '>Intervalo de Preços</h1>", unsafe_allow_html=True)
        st.write("É a diferença entre o maior preço e o menor preço.")
        st.markdown("<h5 style='text-align: rigth; color:khaki '>Média de Preços</h1>", unsafe_allow_html=True)
        st.write("É o valor médio dos preços.")
        st.write("A média é obtida pela soma de todos os preços do conjunto de dados e divide-se pela quantidade de preços no conjunto.")
        st.markdown("<h5 style='text-align: rigth; color:khaki '>Mediana dos Preços</h1>", unsafe_allow_html=True)
        st.write("É a mediana dos preços.")
        st.write("A mediana é o valor central do conjunto de dados.")
        st.markdown("<h5 style='text-align: rigth; color:khaki '>Desvio Padrão</h1>", unsafe_allow_html=True)
        st.write("O desvio padrão é uma medida que expressa o grau de dispersão de um conjunto de dados. Ou seja, o desvio padrão indica o quanto um conjunto de dados é uniforme. Quanto mais próximo de 0 for o desvio padrão, mais homogêneo são os dados.")
        st.markdown("<h5 style='text-align: rigth; color:khaki '>Skewness (Distorção) </h1>", unsafe_allow_html=True)
        st.write("É o afastamento de todos os valores de uma série em relação a média aritmética ou mediana.")
        st.write("Distribuição com base no valor de assimetria: \n - Skewness = 0: Então normalmente distribuído. \n - Skewness > 0: Então mais peso na cauda esquerda da distribuição. \n - Skewness < 0: Então mais peso na cauda direita da distribuição.")
        st.markdown("<h5 style='text-align: rigth; color:khaki '>Kurtosis</h1>", unsafe_allow_html=True)
        st.write("É o grau de desvio ou afastamento da simetria de uma distribuição.")
        st.write("- Kurtosis para distribuição normal é igual a 3. \n - Para uma distribuição com Kurtosis < 3: é chamada platicúrtica e significa que a distribuição é mais achatada que a normal. \n - Para uma distribuição com Kurtosis > 3, é chamada de leptocúrtica e significa que a distribuição é mais pontiaguda que a normal.")

def graphic():
    st.markdown("<h4 style='text-align: center; '>Filtros do Gráfico</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        r_store = st.radio("Lojas", ('Todas', 'H&M', 'Macys'))

    with col2:
        r_x_comparison = st.radio ("Valores para X", ('Estilo', 'Composição', 'Preço'), index=0)

    with col3:
        r_y_comparison = st.radio ("Valores para Y", ('Estilo', 'Composição', 'Preço'), index=2)

    with st.container():
        st.plotly_chart(scatter_plot(r_store, r_x_comparison, r_y_comparison))

def foot():
     st.markdown("<h2 style='text-align: center; '>Conclusão</h1>", unsafe_allow_html=True)
     st.write("Durante a obtenção dos dados pude perceber que há uma diferença de público-alvo entre as duas lojas, a H&M é uma loja mais focada no público de menor poder aquisitivo e a Macys é mais focada em um público de médio poder aquisitivo, isso é perceptível através do preço geral dos produtos, o valor mais alto da H&M é parecido com o menor valor da Macys. Então a escolha do público-alvo do novo empreendimento deve ser algo importante para definição dos produtos oferecidos pela loja ou se ela vai tentar atrair os dois tipos de público de uma vez.")
     st.write("Para mais detalhes sobre o projeto e insights, entre no meu [portifólio](https://gustavomichelsen.github.io/portifolio_projetos/web_scraping.html).")

if __name__ == "__main__":

    head()
    obj_prog()
    data_desc()
    graphic()
    foot()