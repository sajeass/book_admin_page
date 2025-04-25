import streamlit as st
import pandas as pd
import uuid
from src.common._database import Database
from src.common._file_control import File_control

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

def insert_expert(data) -> int:
    query = """
        INSERT INTO z_expert
        (group_name, group_code, expert_name, phone_num, coverage_region, coverage_use,
         keyword, detail_info, coment, img_url, business_card_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    st.session_state.db.insert(query, data)
    result = st.session_state.db.select_one("SELECT LAST_INSERT_ID()")
    return result[0] if result else None

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

with right_col:
    st.subheader("📝 전문가 정보 입력" if is_new else "✏️ 전문가 정보 수정")

    if expert_data["img_url"]:
        st.markdown("### 🖼️ 대표사진")
        st.markdown(
            f'<a href="{expert_data["img_url"]}" target="_blank">'
            f'<img src="{expert_data["img_url"]}" width="300"/></a>',
            unsafe_allow_html=True
        )
        if st.button("🗑️ 대표사진 삭제"):
            blob_path = expert_data["img_url"].split(".net/")[-1]
            fc = File_control(
                file_name=blob_path.split("/")[-1],
                container_name="expert-profile",
                blob_path=blob_path
            )
            if fc.check_file_exists():
                fc.blob_service_client.get_blob_client(fc.container_name, fc.blob_path).delete_blob()
            st.session_state.db.insert(f"UPDATE z_expert SET img_url='' WHERE id={selected_id}")
            st.success("✅ 대표사진이 삭제되었습니다.")
            st.cache_data.clear()
            st.rerun()


        if expert_data["business_card_url"]:
            st.markdown("### 💳 명함사진")
            st.markdown(
                f'<a href="{expert_data["business_card_url"]}" target="_blank">'
                f'<img src="{expert_data["business_card_url"]}" width="300"/></a>',
                unsafe_allow_html=True
            )
            if st.button("🗑️ 명함사진 삭제"):
                blob_path = expert_data["business_card_url"].split(".net/")[-1]
                fc = File_control(
                    file_name=blob_path.split("/")[-1],
                    container_name="expert-card",
                    blob_path=blob_path
                )
                if fc.check_file_exists():
                    fc.blob_service_client.get_blob_client(fc.container_name, fc.blob_path).delete_blob()
                st.session_state.db.insert(f"UPDATE z_expert SET business_card_url='' WHERE id={selected_id}")
                st.success("✅ 명함사진이 삭제되었습니다.")
                st.cache_data.clear()
                st.rerun()


                
    with st.form("expert_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            group_name = st.selectbox("그룹 이름 *", ["대출 상담사","컨설턴트","법무사","중개사"], index=0 if expert_data["group_name"] != "그외" else 1)
            group_code = "1" if group_name == "대출 상담사" else "2"

            expert_name = st.text_input("전문가 이름 *", expert_data["expert_name"], placeholder="예: 홍길동")
            phone_num = st.text_input("핸드폰 번호", expert_data["phone_num"], placeholder="예: 010-1234-5678")
            coverage_region = st.text_input("대표 지역", expert_data["coverage_region"], placeholder="예: 전국, 서울, 경기 등")
            coverage_use = st.text_input("대표 물건", expert_data["coverage_use"], placeholder="예: 모든 물건, 아파트, 토지 등")
            rep_img_file = st.file_uploader("대표사진 업로드", type=["jpg", "jpeg", "png"], key="rep_img")

        with col2:
            keyword = st.text_input("키워드 (','로 구분)", expert_data["keyword"], placeholder="예: 경매,NPL,대출")
            detail_info = st.text_area("상세 정보", expert_data["detail_info"], placeholder="키워드 포함 모든 정보 (상담가능시간,등록번호 등등)")
            coment = st.text_area("소개 글", expert_data["coment"], placeholder="전문가 소개 글")
            card_img_file = st.file_uploader("명함사진 업로드", type=["jpg", "jpeg", "png"], key="card_img")

        submitted = st.form_submit_button("등록하기" if is_new else "수정하기")
        
        if submitted:
            if not expert_name:
                st.error("❌ 전문가 이름은 필수 항목입니다.")
                st.stop()

            rep_img_url, card_img_url = expert_data["img_url"], expert_data["business_card_url"]

            if rep_img_file:
                rep_ext = rep_img_file.type.split("/")[-1]
                rep_file_name = f"{uuid.uuid4()}.{rep_ext}"
                fc = File_control(
                    file_name=rep_file_name,
                    container_name="expert-profile",
                    contents=rep_img_file.getvalue(),
                    blob_path=f"profile/{rep_file_name}"
                )
                fc.upload()
                rep_img_url = f"https://{fc.blob_service_client.account_name}.blob.core.windows.net/{fc.container_name}/{fc.blob_path}"

            if card_img_file:
                card_ext = card_img_file.type.split("/")[-1]
                card_file_name = f"{uuid.uuid4()}.{card_ext}"
                fc = File_control(
                    file_name=card_file_name,
                    container_name="expert-card",
                    contents=card_img_file.getvalue(),
                    blob_path=f"card/{card_file_name}"
                )
                fc.upload()
                card_img_url = f"https://{fc.blob_service_client.account_name}.blob.core.windows.net/{fc.container_name}/{fc.blob_path}"

            if is_new:
                expert_id = insert_expert((
                    group_name, group_code, expert_name, phone_num,
                    coverage_region, coverage_use, keyword,
                    detail_info, coment, rep_img_url, card_img_url
                ))
            else:
                expert_id = selected_id
                update_expert((
                    group_name, group_code, expert_name, phone_num,
                    coverage_region, coverage_use, keyword,
                    detail_info, coment, rep_img_url, card_img_url
                ), expert_id)

            st.success("✅ 전문가 정보가 저장되었습니다.")
            st.cache_data.clear()
            st.rerun()
