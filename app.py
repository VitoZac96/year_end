import streamlit as st
import pandas as pd
import numpy as np


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import datetime
import plotly.express as px

import yfinance as yf 

st.title('Year End Rally: S&P 500 Index')
#downloaded = yf.download("^GSPC")

spx = pd.read_excel("sspxx.xlsx", index_col = 0)
#spx = downloaded


inizio = st.date_input(
        "Select a starting date",
        datetime.date(2000,1,1),
        min_value = datetime.date(1929,1,1),
        max_value = datetime.date(2023,1,1))


includi = False

col1, col2 = st.columns([1,1])

with col1:
    if st.button("Esclude Best & Worst",type="primary"):
        includi = False
    else:
        includi = True

with col2: 
    if st.button("Include Best & Worst",type="primary"):
        includi = True
    else:
        includi = False


df = pd.DataFrame()
df.index = (pd.date_range("1929-9-30", "1929-12-31")).strftime('%m-%d')
indice_inizio = 82

for year in (spx.index.year.unique()[spx.index.year.unique()>inizio.year]):
    
    data = spx[f"{year}-9":f"{year}-12"]["Adj Close"].pct_change()[f"{year}-9-30":]
    data.index = data.index.strftime('%m-%d')
    
    df[f"{year}"] = data
    
df.iloc[0,:]= 0

rit_medio = np.cumprod(1+df.mean(axis = 1)).fillna(method='ffill')#.dropna())
rit_cum_medio = np.cumprod(1+df.mean(axis = 1)).fillna(method='ffill')
ritorno_24 = np.cumprod(1+df["2024"]).fillna(method='bfill')
rit_cum_24 = np.cumprod(1+df["2024"]).fillna(method='bfill').dropna()
ritorni_cumulati = np.cumprod(1+df).fillna(method='ffill')


minimo = ritorni_cumulati.iloc[-1,:].min()
massimo = ritorni_cumulati.iloc[-1,:].max()
min_cumprod = ritorni_cumulati.loc[:,ritorni_cumulati.iloc[-1,:] == ritorni_cumulati.iloc[-1,:].min()].dropna().iloc[:,0]
max_cumprod = ritorni_cumulati.loc[:,ritorni_cumulati.iloc[-1,:] == ritorni_cumulati.iloc[-1,:].max()].dropna().iloc[:,0]


df_plot = pd.DataFrame()
df_plot["Average"] = rit_medio
df_plot["2024"] = rit_cum_24

if includi == True:
    df_plot["Best"] = max_cumprod
    df_plot["Worst"] = min_cumprod

df_plot.index = (pd.date_range("2024-9-30", "2024-12-31")).strftime('%d-%m-%Y')


fig_interactive = px.line(df_plot,title='Value of 1$ invested on the 30th of september')
fig_interactive.add_vline(x="25-11-2024", line_width=1, line_dash="dash", line_color="green")
#fig.add_vline(x = "25-11-2024")

fig_interactive.update_layout(
        title=dict(
            text='Value of 1$ invested on the 30th of september'
        ),
        xaxis=dict(
            title=dict(
                text='Day'
            )
        ),
        yaxis=dict(
            title=dict(
                text='Value'
            )
        ),
)


st.header(f"Average year end rally from {inizio.year}")
st.plotly_chart(fig_interactive)


st.subheader("Results")
st.subheader(f"Average year end rally from {inizio.year}: {(rit_cum_medio[-1]-1)*100:.3}%", divider=True)
st.subheader(f"Best year end rally: {max_cumprod.name}: {(max_cumprod[-1]-1)*100:.3}%", divider=True)
st.subheader(f"Worst year end rally: {min_cumprod.name}: {(min_cumprod[-1]-1)*100:.3}%", divider=True)


#
