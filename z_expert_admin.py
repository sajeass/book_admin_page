import streamlit as st
import pandas as pd
from src.common._database import Database

st.set_page_config(page_title="z_expert 전문가 관리", layout="wide")
st.title("📇 전문가 관리 페이지")

# ✅ DB 연결
if "db" not in st.session_state:
    st.session_state.db = Database(schema="aboutb_pro4")

COLUMNS = [
    "id", "group_name", "group_code", "expert_name", "phone_num",
    "coverage_region", "coverage_use", "keyword", "detail_info",
    "coment", "img_url", "business_card_url", "insert_time", "uupdate_time"
]

@st.cache_data(ttl=60)
def load_expert_list():
    rows = st.session_state.db.select_all("SELECT * FROM z_expert ORDER BY id DESC")
    return pd.DataFrame(rows, columns=COLUMNS) if rows else pd.DataFrame(columns=COLUMNS)

@st.cache_data(ttl=60)
def get_expert_by_id(expert_id):
    row = st.session_state.db.select_one(f"SELECT * FROM z_expert WHERE id = {expert_id}")
    return dict(zip(COLUMNS, row)) if row else None

def insert_expert(data):
    query = """
        INSERT INTO z_expert
        (group_name, group_code, expert_name, phone_num, coverage_region, coverage_use,
         keyword, detail_info, coment, img_url, business_card_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    st.session_state.db.insert(query, data)

def update_expert(data, expert_id):
    query = """
        UPDATE z_expert SET
        group_name=%s, group_code=%s, expert_name=%s, phone_num=%s,
        coverage_region=%s, coverage_use=%s, keyword=%s, detail_info=%s,
        coment=%s, img_url=%s, business_card_url=%s,
        uupdate_time=NOW()
        WHERE id = %s
    """
    st.session_state.db.insert(query, data + (expert_id,))

# --- 데이터 조회
df = load_expert_list()
left_col, right_col = st.columns([1, 2])

# --- 좌측: 전문가 선택 + 등록
with left_col:
    options = ["➕ 새 전문가 등록"] + (df["expert_name"] + " (" + df["id"].astype(str) + ")").tolist()
    selected = st.radio("전문가 선택", options)
    is_new = selected.startswith("➕")
    selected_id = None if is_new else int(selected.split("(")[-1].replace(")", ""))

    expert_data = {
        "group_name": "", "group_code": "", "expert_name": "", "phone_num": "",
        "coverage_region": "", "coverage_use": "", "keyword": "", "detail_info": "",
        "coment": "", "img_url": "", "business_card_url": ""
    }

    if selected_id:
        loaded = get_expert_by_id(selected_id)
        if loaded:
            expert_data.update(loaded)

# --- 우측: 폼 공통
with right_col:
    st.subheader("📝 전문가 정보 입력" if is_new else "✏️ 전문가 정보 수정")

    with st.form("expert_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            group_name = st.text_input("그룹 이름", expert_data["group_name"])
            group_code = st.text_input("그룹 코드", expert_data["group_code"])
            expert_name = st.text_input("전문가 이름", expert_data["expert_name"])
            phone_num = st.text_input("핸드폰 번호", expert_data["phone_num"])
            coverage_region = st.text_input("대표 지역", expert_data["coverage_region"])
            coverage_use = st.text_input("대표 물건", expert_data["coverage_use"])
        with col2:
            keyword = st.text_input("키워드 (','로 구분)", expert_data["keyword"])
            detail_info = st.text_area("상세 정보", expert_data["detail_info"])
            coment = st.text_area("코멘트", expert_data["coment"])
            img_url = st.text_input("이미지 URL", expert_data["img_url"])
            business_card_url = st.text_input("명함 이미지 URL", expert_data["business_card_url"])

        submitted = st.form_submit_button("등록하기" if is_new else "수정하기")
        if submitted:
            data_tuple = (
                group_name, group_code, expert_name, phone_num,
                coverage_region, coverage_use, keyword,
                detail_info, coment, img_url, business_card_url
            )
            if is_new:
                insert_expert(data_tuple)
                st.success("✅ 전문가가 등록되었습니다.")
            else:
                update_expert(data_tuple, selected_id)
                st.success("✅ 전문가 정보가 수정되었습니다.")
            st.cache_data.clear()
            st.rerun()
