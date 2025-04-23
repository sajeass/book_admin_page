import streamlit as st
import requests
from src.common.mongo_database import MongoDB
from src.common._database import Database

st.set_page_config(layout="wide")
st.title("📑 건축물대장 매칭 관리자")

LAMBDA_URL = "https://3bljfdmys2jwtyhdq3i74i32ne0yadtn.lambda-url.ap-northeast-2.on.aws/"

# ✅ 데이터베이스 객체를 한 번만 생성하여 사용
if "db" not in st.session_state:
    st.session_state.db = Database(schema='aboutb_pro4')

if "mongo_db" not in st.session_state:
    st.session_state.mongo_db = MongoDB()

# --- 그룹 선택 (일반건축물 / 전유건축물) ---
group_type = st.radio("건축물 유형 선택", ["일반건축물", "전유건축물"], horizontal=True, index=0)

# ✅ 페이지네이션을 위한 초기 상태값 설정
if "page_no" not in st.session_state:
    st.session_state.page_no = 1  # 기본 페이지 1

@st.cache_data(ttl=60)  # 60초 동안 캐시 유지
def fetch_items_and_count(group, page_no):
    offset = (page_no - 1) * 100
    db = st.session_state.db

    query = f"""
        SELECT i_code,dongnm FROM i_request 
        WHERE progress_type = '1' 
        AND {'ilban_pk' if group == '일반건축물' else 'junyu_pk'} = ''  
        {f"AND ilban_pk NOT IN ('0', '') AND i_class_code = '3'" if group == '전유건축물' else ""}
        LIMIT 100 OFFSET {offset}
    """
    items = db.select_all(query)

    count_query = f"""
        SELECT COUNT(*) FROM i_request 
        WHERE progress_type = '1' 
        AND {'ilban_pk' if group == '일반건축물' else 'junyu_pk'} = ''  
        AND {'ilban_pk' if group == '일반건축물' else 'junyu_pk'} != '0'
        {f"AND ilban_pk NOT IN ('0', '') AND i_class_code = '3'" if group == '전유건축물' else ""}
    """
    total_count = db.select_one(count_query)[0]

    return [(item[0], item[1]) for item in items], total_count

# ✅ 데이터 가져오기 (속도 개선)
items_list, total_items_count = fetch_items_and_count(group_type, st.session_state.page_no)

st.subheader(f"📋 매칭 대상 (전체: {total_items_count}개, 현재 페이지: {len(items_list)}개)")

# ✅ 선택된 물건 추적
if "selected_index" not in st.session_state:
    st.session_state.selected_index = 0

if "selected_i_code" not in st.session_state:
    st.session_state.selected_i_code = None  # ✅ 기본값 설정

if "selected_dongnm" not in st.session_state:  # ✅ dongnm 초기화
    st.session_state.selected_dongnm = None
    
# ✅ MongoDB 조회 캐싱
@st.cache_data(ttl=60)
def fetch_mongo_data(i_code):
    mongo_db = st.session_state.mongo_db
    query = {"i_code": i_code}
    return mongo_db.find_one("court_auction", 'progress_items', query)

def fetch_dongnm_sql(i_code):
    "SELECT dongnm FROM aboutb_pro4.i_request where i_code = %s"
    return result

# ✅ Lambda API 데이터 캐싱 (30초 동안 동일 요청 방지)
@st.cache_data(ttl=60)
def fetch_api_candidates(request_payload):
    response = requests.post(LAMBDA_URL, json=request_payload)
    if response.status_code == 200:
        return response.json().get("result", [])
    return []

# 화면을 세 개의 컬럼으로 나누기
left_col, mid_col, right_col = st.columns([1, 2, 2])

# ✅ left_col: 매칭할 물건 선택
with left_col:
    if items_list:
        selected_idx = st.radio(
            "물건 선택",
            options=range(len(items_list)),
            index=next((i for i, (code, dong) in enumerate(items_list) 
                        if code == st.session_state.selected_i_code and dong == st.session_state.selected_dongnm), 0),  
            format_func=lambda x: items_list[x][0]  # ✅ i_code만 표시
        )

        selected_i_code, selected_dongnm = items_list[selected_idx]  # ✅ 선택된 항목에서 dongnm 가져오기

        if selected_i_code != st.session_state.selected_i_code:
            st.session_state.selected_i_code = selected_i_code
            st.session_state.selected_dongnm = selected_dongnm  # ✅ dongnm 값 저장 (빈 값도 포함)
            st.session_state.api_candidates = None  # ✅ 새 물건 선택 시 후보 초기화

if st.session_state.selected_i_code:
    item = fetch_mongo_data(st.session_state.selected_i_code)

with mid_col:
    if item:
        jibun_code = item.get("address", {}).get("jibun_addr_code", "")
        my_property_info = {
            "주소": item.get("i_original_juso", ""),
            "건물명": item.get("bldNm", ""),
            "동호수": item.get("bldDtlDts", ""),
            "등기상 면적": str(item.get("court_extra", {}).get("build_area_float", "")) + "m²",
            "i_class_code": item.get("i_class_code", ""),
            "m_code": item.get("m_code", ""),
        }
        m_code = item.get("m_code", "")
        if m_code:
            detail_url = f"https://madangs.com/caview?m_code={m_code}"
            st.markdown(f"[🔗 상세페이지 바로가기]({detail_url})", unsafe_allow_html=True)
            
        with st.expander("📋 선택된 기본정보 보기", expanded=True):
            st.json(my_property_info)

with right_col:
    # ✅ 선택된 물건이 유지되도록 설정 (초기화 방지)
    if "selected_i_code" not in st.session_state or st.session_state.selected_i_code is None:
        st.session_state.selected_i_code = selected_i_code  # 현재 선택된 물건을 유지

    # ✅ Lambda API 데이터 한 번만 가져오고 재사용
    if st.session_state.selected_i_code is not None and st.session_state.get("api_candidates") is None:
        request_payload = {
            "request_type": "admin_ilban_api" if group_type == "일반건축물" else "admin_junyu_api",
            "jibun_code": jibun_code,
            "page_no": st.session_state.page_no
        }
        # ✅ 전유건축물일 경우, dongnm 추가
        if group_type == "전유건축물":
            request_payload["dongnm"] = st.session_state.selected_dongnm  

        st.session_state.api_candidates = fetch_api_candidates(request_payload)

    api_candidates = st.session_state.api_candidates
    candidate_details = None  # ✅ 기본값 설정

    if api_candidates:
        st.subheader(f"📌 건축물대장 후보 ({len(api_candidates)}개)")

        # ✅ "후보 선택" 라디오 버튼을 버튼 아래 배치
        with st.container():
            selected_index = st.radio(
                "후보 선택",
                options=range(len(api_candidates)),
                index=0 if len(api_candidates) > 0 else None,  # ✅ 예외 처리 추가
                format_func=lambda x: f"{api_candidates[x].get('newPlatPlc', '')} - "
                                      f"{api_candidates[x].get('bldNm', '')} "
                                      f"({api_candidates[x].get('dongNm', '') if group_type == '일반건축물' else api_candidates[x].get('hoNm', '').strip() or '호정보 없음'})"
            )
            candidate_details = api_candidates[selected_index] if api_candidates else None

    # ✅ 버튼을 항상 표시되도록 변경
    col1, col2, col3 = st.columns([2, 1, 1])

    def move_to_next():
        """다음 물건을 자동 선택 & 매칭 대상 최신화"""
        st.session_state.selected_index = 0  # 새 물건 선택 시 후보 리스트 초기화
        st.session_state.selected_i_code = None  # ✅ 다음 물건을 선택하도록 설정
        st.session_state.api_candidates = None  # ✅ 후보 개수 업데이트 (다시 API 호출)
        st.session_state.items_list = None  # ✅ 매칭 대상 물건 최신화 (다시 DB 조회)
        st.rerun()  # ✅ 버튼 클릭 후 리프레시

    with col1:
        if st.button("✅ 매칭 확정", use_container_width=True, disabled=candidate_details is None):
            if candidate_details:
                match_payload = {
                    "request_type": "admin_junyu_match" if group_type == "전유건축물" else "admin_ilban_match",
                    "i_code": st.session_state.selected_i_code,
                    "jibun_code": jibun_code,
                    "junyu_info" if group_type == "전유건축물" else "ilban_info": candidate_details
                }
                match_response = requests.post(LAMBDA_URL, json=match_payload)

                if match_response.status_code == 200:
                    st.success(f"✅ 매칭 완료: {candidate_details['newPlatPlc']} - {candidate_details['bldNm']}")
                    move_to_next()
                else:
                    st.error("❌ 매칭 실패: 서버 오류 발생")

    with col2:
        if st.button("❌ PASS", use_container_width=True):
            db = Database(schema='aboutb_pro4')
            update_query = f"""
                UPDATE i_request
                SET {'ilban_pk' if group_type == "일반건축물" else "junyu_pk"} = '0'
                WHERE i_code = {st.session_state.selected_i_code}
            """
            db.insert(update_query)
            st.warning(f"🚨 PASS 완료: i_code {st.session_state.selected_i_code} ({'ilban_pk' if group_type == "일반건축물" else "junyu_pk"}=0 설정됨)")
            move_to_next()

    with col3:
        if st.button("➡️ 다음 페이지", use_container_width=True):
            st.session_state.page_no += 1  # ✅ 페이지 증가
            st.session_state.api_candidates = None  # ✅ API 후보 리스트 초기화

            # ✅ 특정 영역(right_col)만 업데이트: UI 전체 새로고침 방지
            with right_col.empty():  # 🔹 기존 UI를 비우고 업데이트
                # 🔹 API 후보 리스트가 None이면 즉시 갱신
                st.session_state.api_candidates = fetch_api_candidates({
                    "request_type": "admin_ilban_api" if group_type == "일반건축물" else "admin_junyu_api",
                    "jibun_code": jibun_code,
                    "page_no": st.session_state.page_no
                })

                # ✅ API 후보 리스트가 업데이트된 상태로 다시 UI 렌더링
                st.subheader(f"📌 건축물대장 후보 ({len(st.session_state.api_candidates)}개)")

    # 🔹 선택된 후보 정보를 `expander`로 출력
    if candidate_details:
        with st.expander("📋 선택된 건축물 정보 보기", expanded=True):
            st.json(candidate_details)
















