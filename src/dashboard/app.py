import streamlit as st
import pandas as pd
import sqlite3

#conectar com o banco de dados
conn = sqlite3.connect('../../data/quotes.db')

#carregar dados do banco em um DF
df = pd.read_sql_query("SELECT * FROM mercadolivre_items", conn)

#fechar conexao com banco
conn.close()

#Titulo da aplicação
st.title('Pesquisa de Mercado - Tênis Esportivos no Mercado Livre')

#Dividindo a tela em colunas
st.subheader("KPI'S principais do sistema")
col1,col2,col3 = st.columns(3)

#KPI 1: Numero total de itens
total_items = df.shape[0]
col1.metric(label='Número total de itens', value=total_items)

#KPI 2: Numero de marcas únicas
unique_brands = df['brand'].nunique()
col2.metric(label='Número de marcas únicas', value=unique_brands)

#KPI 3: Preço médio novo (em reais)
average_new_price = df['new_price'].mean()
col3.metric(label='Preço médio novo', value=f'{average_new_price:.2f}')

#Marcas mais encontradas até a página 10
st.subheader("Marcas mais encontradas até a página 10")
col1,col2 = st.columns([4,2])
top_10_pages_brand = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_pages_brand)
col2.write(top_10_pages_brand)

#Preço médio por marca
st.subheader("Preço médio por marca")
col1,col2 = st.columns([4,2])
df_non_zero_price = df[df['new_price'] > 0]
average_price_by_brand = df_non_zero_price.groupby('brand')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(average_price_by_brand)
col2.write(average_price_by_brand)

#Satisfação por marca
st.subheader("Satisfação por marca")
col1,col2 = st.columns([4,2])
df_non_zero_reviews = df[df['reviews_rating_number'] > 0]
satisfaction_by_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)
