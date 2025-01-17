#!/usr/bin/env python
# coding: utf-8

# In[2]:


# pip install streamlit fbprophet yfinance plotly
import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2000-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stock Forecast App')

stocks = ('inta', 'inta', 't', 'hpe', 'shop', 'nok', 'dv', 'docu', 'pltr', 'GOOG', 'AAPL', 'nvda', 'voo', 'META', 'XOM', 'CVX', 'TSLA', 'JPM', 'CRM', 'MA', 'AMD', 'REAX', 'COUR', 'IAS', 'YEXT', 'LZ', 'XPOF', 'CLOV', 'ASUR', 'IMMR', 'SMRT', 'SMCI', 'PAYO', 'SOFI', 'SOUN', 'MSCI', 'ORLY', 'IPAR', 'KNSL', 'GLOB', 'MTLS', 'ARDX', 'SERA', 'ICU', 'MTEX', 'LRMR', 'INLX', 'TME', 'CLVT', 'IQ', 'PAGS', 'FSR', 'PIRS', 'YYAI', 'CRKN', 'XOS', 'SLNH', 'BNTC', 'SNCE', 'SMTK', 'MULN', 'ONCT', 'BODI', 'BACK', 'BTTR', 'DTIL', 'VCNX', 'INO', 'TLIS', 'TBLT', 'CGC', 'AKTX', 'ADXN', 'ZVSA', 'CATX', 'VHC', 'ICU', 'MMAT', 'PRPO', 'NCMI', 'SIDU', 'NKE', 'uber'
)
selected_stock = st.selectbox('Select dataset for prediction', stocks)

n_years = st.slider('Days of prediction:', 1, 1826)
period = n_years * 1


@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

	
data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

st.subheader('Raw data')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
plot_raw_data()

# Predict forecast with Prophet.
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast data')
st.write(forecast.tail())
    
st.write(f'Forecast plot for {n_years} days')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)


# In[ ]:




