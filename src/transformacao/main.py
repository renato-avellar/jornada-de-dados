import pandas as pd
import sqlite3
from datetime import datetime

pd.options.display.max_columns = None

df = pd.read_json('../../data/data.json')
df['_source'] = "https://lista.mercadolivre.com/tenis-corrida-masculino"
df['_data_coleta'] = datetime.now()

df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_cents'] = df['old_price_cents'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_cents'] = df['new_price_cents'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

#Tirando os parenteses dos numeros
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

#juntando os reais com centavos
df['old_price'] = df['old_price_reais'] + df['old_price_cents'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_cents'] / 100

#deletando as colunas de valores antigas
df = df.drop(columns=['old_price_reais', 'old_price_cents', 'new_price_reais', 'new_price_cents'])

#conectar ao sqlite3
conn = sqlite3.connect('../../data/quotes.db')
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

#fechar conexao
conn.close()