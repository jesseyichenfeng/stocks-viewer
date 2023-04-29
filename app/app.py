# a streamlit app that take two stock ticker and two dates, a starting date and ending date. Assume I invest each stock with 10k dollar.

import streamlit as st
import yfinance as yf
import numpy as np

#merge two ticker data assume invest each stock with 10k dollar
def merge_two_tickers(tickerSymbol1, tickerSymbol2, start_date, end_date):
    tickerData1 = yf.Ticker(tickerSymbol1).history(period='1d', start=start_date, end=end_date)
    tickerData2 = yf.Ticker(tickerSymbol2).history(period='1d', start=start_date, end=end_date)
    tickerData1['Close'] = 10000/tickerData1['Close'].iloc[0]*tickerData1['Close']
    tickerData2['Close'] = 10000/tickerData2['Close'].iloc[0]*tickerData2['Close']
    tickerData1 = tickerData1[['Close']].rename(columns={'Close': tickerSymbol1})
    tickerData2 = tickerData2[['Close']].rename(columns={'Close': tickerSymbol2})

    df = tickerData1.join(tickerData2, how='inner')

    df2 = df.copy()

    df2['tickerSymbol1_return'] = df2[tickerSymbol1].pct_change(20)
    df2['tickerSymbol2_return'] = df2[tickerSymbol2].pct_change(20)

    df.dropna(inplace=True)

    df2.dropna(inplace=True)

    cov_matrix = np.cov(df2['tickerSymbol1_return'], df2['tickerSymbol2_return'])

    # Calculate the variance of the daily returns of stock1
    stock1_var = df2['tickerSymbol1_return'].var()

    # Calculate beta of stock2 with respect to stock1
    beta_stock2 = cov_matrix[0][1] / stock1_var

    return df, beta_stock2



#Input ticker and date range
tickerSymbol1 = st.text_input("Enter ticker A", "^GSPC")
tickerSymbol2 = st.text_input("Enter ticker B", "MSFT")
start_date = st.text_input("Enter start date", "2010-5-31")
end_date = st.text_input("Enter end date", "2020-5-31")


#merge two ticker data
df,beta = merge_two_tickers(tickerSymbol1, tickerSymbol2, start_date, end_date)

# a streamlit submit button, if click run st.line_chart(df)
if st.button('Submit'):
    st.line_chart(df)

    #streamlit show percentage change of each stock
    st.write(tickerSymbol1, '->', str(round((df[tickerSymbol1].iloc[-1]-df[tickerSymbol1].iloc[0])/df[tickerSymbol1].iloc[0]*100, 2))+'%')
    st.write(tickerSymbol2, '->', str(round((df[tickerSymbol2].iloc[-1]-df[tickerSymbol2].iloc[0])/df[tickerSymbol2].iloc[0]*100, 2))+'%')

    st.write('Beta of', tickerSymbol2, '->', round(beta, 2))

