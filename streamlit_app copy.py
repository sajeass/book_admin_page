import streamlit as st
import requests
from src.common.mongo_database import MongoDB
from src.common._database import Database

st.set_page_config(layout="wide")
st.title("📑 건축물대장 매칭 관리자")

LAMBDA_URL = "https://3bljfdmys2jwtyhdq3i74i32ne0yadtn.lambda-url.ap-northeast-2.on.aws/"

mongo_db = MongoDB()
db = Database(schema='aboutb_pro4')

# --- 그룹 선택 (일반건축물 / 전유건축물) ---
group_type = st.radio("건축물 유형 선택", ["일반건축물", "전유건축물"], horizontal=True, index=0)

# ✅ 페이지네이션을 위한 초기 상태값 설정 (전유건축물만)
if "page_no" not in st.session_state:
    st.session_state.page_no = 1  # 기본 페이지 1

@st.cache_data(ttl=60)  # 60초 동안 캐시 유지 (필요에 따라 조정 가능)
def fetch_items_and_count(group, page_no):
    offset = (page_no - 1) * 100
    query = f"""
        SELECT i_code FROM i_request 
        WHERE progress_type = '1' 
        AND {'ilban_pk' if group == '일반건축물' else 'junyu_pk'} = ''  
        AND {'ilban_pk' if group == '일반건축물' else 'junyu_pk'} != '0'
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

    return [item[0] for item in items], total_count

# ✅ 데이터 가져오기 (속도 개선)
items_list, total_items_count = fetch_items_and_count(group_type, st.session_state.page_no)


st.subheader(f"📋 매칭 대상 (전체: {total_items_count}개, 현재 페이지: {len(items_list)}개)")

# ✅ st.session_state를 활용하여 현재 선택된 물건 추적
if "selected_index" not in st.session_state:
    st.session_state.selected_index = 0

# 화면을 세 개의 컬럼으로 나누기
left_col, mid_col, right_col = st.columns([1, 2, 2])

with left_col:
    if items_list:
        selected_i_code = st.radio(
            "물건 선택",
            options=range(len(items_list)),
            index=st.session_state.selected_index,
            format_func=lambda x: items_list[x]
        )
    else:
        st.warning("❌ 매칭할 대상이 없습니다.")
        selected_i_code = None

with mid_col:
    if selected_i_code is not None:
        i_code = items_list[selected_i_code]

        mongo_db = MongoDB()
        query = {"i_code": i_code}
        item = mongo_db.find_one("court_auction", 'progress_items', query)
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

            st.subheader("🔍 기본정보")
            st.json(my_property_info)

            m_code = item.get("m_code", "")
            if m_code:
                detail_url = f"https://madangs.com/caview?m_code={m_code}"
                st.markdown(f"[🔗 상세페이지 바로가기]({detail_url})", unsafe_allow_html=True)
            else:
                st.warning("🔍 m_code 정보가 없습니다.")
        else:
            st.error("MongoDB 데이터 없음")

with right_col:
    # ✅ Lambda API 데이터 캐싱 (30초 동안 동일 요청 방지)
    @st.cache_data(ttl=30)
    def fetch_api_candidates(request_payload):
        response = requests.post(LAMBDA_URL, json=request_payload)
        if response.status_code == 200:
            return response.json().get("result", [])
        return []

    # ✅ 기본정보 및 후보 정보를 세션 상태에 저장하여 다시 로드 방지
    if "selected_i_code" not in st.session_state:
        st.session_state.selected_i_code = None
    if "selected_candidate" not in st.session_state:
        st.session_state.selected_candidate = None
    if "api_candidates" not in st.session_state:
        st.session_state.api_candidates = None

    if selected_i_code is not None:
        request_payload = {
            "request_type": "admin_ilban_api" if group_type == "일반건축물" else "admin_junyu_api",
            "jibun_code": jibun_code
        }
        if group_type == "전유건축물":
            request_payload["page_no"] = st.session_state.page_no

        api_candidates = fetch_api_candidates(request_payload)

        response = requests.post(LAMBDA_URL, json=request_payload)

        if response.status_code == 200:
            result = response.json()
            api_candidates = result["result"]

            if api_candidates:
                st.subheader(f"📌 건축물대장 후보 ({len(api_candidates)}개)")

                if group_type == "일반건축물":
                    selected_index = st.radio(
                        "후보 선택",
                        options=range(len(api_candidates)),
                        format_func=lambda x: f"{api_candidates[x]['newPlatPlc']} - {api_candidates[x]['bldNm']} ({api_candidates[x]['dongNm']})"
                    )
                    candidate_details = api_candidates[selected_index]
        
                    with st.expander("📋 선택된 건축물 정보 보기", expanded=True):  # 기본으로 펼쳐진 상태
                        st.json({
                        "도로명 주소": candidate_details.get('newPlatPlc', '') or '',
                        "건물명": candidate_details.get('bldNm', '') or '',
                        "동명": candidate_details.get('dongNm', '') or '',
                        "주용도": candidate_details.get('etcPurps', '') or '',
                        "구조": candidate_details.get('strctCdNm', '') or '',
                        "면적(㎡)": candidate_details.get('archArea', '') or '',
                        "사용승인일": candidate_details.get('useAprDay', '') or '',
                        "지상층 수": candidate_details.get('grndFlrCnt', 0) or '',
                        "지하층 수": candidate_details.get('ugrndFlrCnt', 0) or '',
                    })
                
                else:
                    selected_index = st.radio(
                        "후보 선택",
                        options=range(len(api_candidates)),
                        format_func=lambda x: f"{api_candidates[x].get('newPlatPlc', '')} - {api_candidates[x].get('bldNm', '')} ({api_candidates[x].get('hoNm', '').strip() or '호정보 없음'})"
                    )


                    candidate_details = api_candidates[selected_index]
                    with st.expander("📋 선택된 건축물 정보 보기", expanded=True):  # 기본으로 펼쳐진 상태
                        st.json({
                        "도로명 주소": candidate_details.get('newPlatPlc', '') or '',
                        "건물명": candidate_details.get('bldNm', '') or '',
                        "동명": candidate_details.get('dongNm', '') or '',
                        "호명": candidate_details.get('hoNm', '') or '',
                        "주용도": candidate_details.get('etcPurps', '') or '',
                        "구조": candidate_details.get('strctCdNm', '') or '',
                        "면적(㎡)": candidate_details.get('area', '') or '',
                        "사용승인일": candidate_details.get('useAprDay', '') or '',
                    })


                # ✅ 전유건축물일 경우에만 페이지네이션 버튼 표시
                if group_type == "전유건축물":
                    page_col1, page_col2 = st.columns([1, 1])
                    with page_col1:
                        if st.session_state.page_no > 1 and st.button("⬅️ 이전 페이지"):
                            st.session_state.page_no -= 1
                            st.rerun()
                    with page_col2:
                        if st.button("➡️ 다음 페이지"):
                            st.session_state.page_no += 1
                            st.rerun()

                # 🔹 "매칭 확정" 및 "PASS" 버튼
                match_col, pass_col = st.columns([2, 1])

                def move_to_next():
                    """다음 물건을 자동 선택"""
                    st.session_state.selected_index = (st.session_state.selected_index + 1) % len(items_list)
                    st.rerun()

                with match_col:
                    if st.button("✅ 매칭 확정"):
                        match_payload = {
                            "request_type": "admin_junyu_match" if group_type == "전유건축물" else "admin_ilban_match",
                            "i_code": i_code,
                            "jibun_code": jibun_code,
                            "junyu_info" if group_type == "전유건축물" else "ilban_info": candidate_details
                        }

                        match_response = requests.post(LAMBDA_URL, json=match_payload)

                        if match_response.status_code == 200:
                            st.success(f"✅ 매칭 완료: {candidate_details['newPlatPlc']} - {candidate_details['bldNm']}")
                            move_to_next()
                        else:
                            st.error("❌ 매칭 실패: 서버 오류 발생")

                with pass_col:
                    if st.button("❌ PASS"):
                        db = Database(schema='aboutb_pro4')
                        update_query = f"""
                            UPDATE i_request 
                            SET {'ilban_pk' if group_type == '일반건축물' else 'junyu_pk'} = '0' 
                            WHERE i_code = {i_code}
                        """
                        db.insert(update_query)
                        st.warning(f"🚨 PASS 완료: i_code {i_code} ({'ilban_pk' if group_type == '일반건축물' else 'junyu_pk'}=0 설정됨)")
                        move_to_next()

            else:
                st.warning("API 조회 결과 없음")
        else:
            st.error("API 호출 실패")

