import streamlit as st
import pandas as pd
from src.common._database import Database
from datetime import datetime

st.set_page_config(page_title="유찰 위험 물건 조회", layout="wide")
st.title("🔍 유찰 위험 물건 조회")

# ✅ DB 연결
if "db" not in st.session_state:
    st.session_state.db = Database(schema="aboutb_pro4")

# ✅ 쿼리 실행
query = """
SELECT m.jiwon_code, m.m_code, m.m_bid_date, m.m_lowest_price, 
       m.m_evaluate_price, m.m_bid_price_last, m.m_sold_price_last, 
       m.m_bid_state, m.m_end_state, m.m_area, m.m_use_type,
       c.c_charge_price
FROM m_basic AS m
JOIN c_basic AS c ON m.c_code = c.c_code
WHERE m.m_state_code = '10'
  AND c.c_charge_price > 0
  AND m.m_lowest_price < c.c_charge_price
ORDER BY m.m_bid_date ASC
"""

rows = st.session_state.db.select_all(query)

if not rows:
    st.warning("❌ 조회된 물건이 없습니다.")
else:
    columns = [
        "법원코드", "물건코드", "입찰일", "최저가", "감정가", 
        "마지막입찰가", "낙찰가", "입찰상태", "진행상태", 
        "면적", "용도", "채권최고액"
    ]
    df = pd.DataFrame(rows, columns=columns)

    # ✅ 날짜 포맷팅 (입찰일)
    if not df.empty and "입찰일" in df.columns:
        df["입찰일"] = pd.to_datetime(df["입찰일"]).dt.strftime("%Y-%m-%d")

    st.dataframe(df, use_container_width=True)

    # ✅ 엑셀 다운로드
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 엑셀 다운로드",
        data=csv,
        file_name=f"유찰위험물건_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
