import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('株価可視化アプリ')

st.sidebar.write("""
# 株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定してください                
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数',1,365,20)

st.write(f"""
### 過去 **{days}日間** の株価
""")

@st.cache_data
def get_data(days,tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name='Name'
        df = pd.concat([df,hist])
    return df

try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)

    ymin, ymax= st.sidebar.slider(
        '範囲を指定してください',
        0.0,20000.0,(0.0,20000.0)
    )

    tickers={
        'Macnica':'3132.T',
        'softbank':'9434.T',
        'sony':'6758.T',
        'TOYOTA':'7203.T',
    }

    df = get_data(days,tickers)
    companies = st.multiselect(
        "会社名を選択してください",
        list(df.index),
        ('Macnica','softbank','sony','TOYOTA')
    )

    if not companies:
        st.error('1社は選択してください')
    else:
        data = df.loc[companies]
        st.write("### 株価",data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value':'株価'}
            )
        
    chart =(
        alt.Chart(data)
        .mark_line(opacity=0.8,clip=True)
        .encode(
            x="Date:T",
            y=alt.Y("株価:Q",stack=None,scale=alt.Scale(domain=[ymin,ymax])),
            color="Name:N"
            )
        )

    st.altair_chart(chart,use_container_width=True)
except:
    st.error(
        "例外が発生しました"
    )