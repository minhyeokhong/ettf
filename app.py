import streamlit as st
import requests
import pandas as pd
from datetime import datetime

def fetch_etf_data():
    url = "https://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    today_date = datetime.today().strftime("%Y%m%d")  # 오늘 날짜
    payload = {
        "bld": "dbms/MDC/STAT/standard/MDCSTAT04601",
        "mktId": "ETF",
        "trdDd": today_date,  # 기준일자 설정
        "share": "1",
        "csvxls_isNo": "false"
    }
    headers = {
        "Authorization": "3BDD2F5006134A0E81FEF61721358426AFFB1DFC "  # API 키 추가
    }
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data['output'])
    else:
        return None

def main():
    st.title("KRX ETF 정보 조회")
    
    df = fetch_etf_data()
    if df is None:
        st.error("KRX API에서 데이터를 가져오지 못했습니다.")
        return
    
    etf_list = df["ISU_NM"].unique()
    selected_etf = st.selectbox("ETF 선택", etf_list)
    
    etf_info = df[df["ISU_NM"] == selected_etf].iloc[0]
    
    st.write("### ETF 기본 정보")
    st.write(f"**종목명:** {etf_info['ISU_NM']}")
    st.write(f"**순자산가치(NAV):** {etf_info['NAV']}")
    st.write(f"**괴리율:** {etf_info['FLUC_RT_IDX']}%")
    st.write(f"**추적오차율:** {etf_info['CMPPREVDD_IDX']}%")
    st.write(f"**PDF:** [다운로드](https://example.com/pdf/{etf_info['ISU_CD']})")

if __name__ == "__main__":
    main()
