import streamlit as st
import requests
from src.common.mongo_database import MongoDB
from src.common._database import Database

st.set_page_config(layout="wide")
st.title("📑 건축물대장 매칭 관리자")

LAMBDA_URL = "https://3bljfdmys2jwtyhdq3i74i32ne0yadtn.lambda-url.ap-northeast-2.on.aws/"

# --- 그룹 선택 (일반건축물 / 전유건축물) ---
group_type = st.radio("건축물 유형 선택", ["일반건축물", "전유건축물"], horizontal=True, index=0)

# ✅ 1) 전체 매칭 대상 개수 가져오기
def get_total_items_count(group):
    db = Database(schema='aboutb_pro4')
    query = f"""
        SELECT COUNT(*) FROM i_request 
        WHERE progress_type = '1' 
        AND {'ilban_pk' if group == '일반건축물' else 'junyu_pk'} = ''  
        AND {'ilban_pk' if group == '일반건축물' else 'junyu_pk'} != '0'
    """
    count_result = db.select_one(query)
    return count_result[0] if count_result else 0

# ✅ 2) 100개씩 가져오는 함수
def load_items_from_mysql(group):
    db = Database(schema='aboutb_pro4')
    query = f"""
        SELECT i_code FROM i_request 
        WHERE progress_type = '1' 
        AND {'ilban_pk' if group == '일반건축물' else 'junyu_pk'} = ''  
        AND {'ilban_pk' if group == '일반건축물' else 'junyu_pk'} != '0' 
        LIMIT 100
    """
    items = db.select_all(query)
    return [item[0] for item in items]

# ✅ 데이터 가져오기
total_items_count = get_total_items_count(group_type)  # 전체 개수
items_list = load_items_from_mysql(group_type)  # 현재 100개

# ✅ 3) Streamlit UI에서 전체 개수 & 현재 페이지 개수 표시
st.subheader(f"📋 매칭 대상 (전체: {total_items_count}개, 현재 페이지: {len(items_list)}개)")
# ✅ `st.session_state`를 활용하여 현재 선택된 물건 추적
if "selected_index" not in st.session_state:
    st.session_state.selected_index = 0

# 화면을 세 개의 컬럼으로 나누기
left_col, mid_col, right_col = st.columns([1, 2, 2])

with left_col:
    # st.subheader(f"📋 매칭 대상 ({len(items_list)}개)")
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

            # ✅ 상세페이지 바로가기 버튼
            m_code = item.get("m_code", "")
            if m_code:
                detail_url = f"https://madangs.com/caview?m_code={m_code}"
                st.markdown(f"[🔗 상세페이지 바로가기]({detail_url})", unsafe_allow_html=True)
            else:
                st.warning("🔍 m_code 정보가 없습니다.")
        else:
            st.error("MongoDB 데이터 없음")

with right_col:
    if selected_i_code is not None and item:
        # 🔹 람다 API 호출 (POST 방식)
        request_type = "admin_ilban_api" if group_type == "일반건축물" else "admin_junyu_api"
        response = requests.post(LAMBDA_URL, json={"request_type": request_type, "jibun_code": jibun_code})

        if response.status_code == 200:
            result = response.json()
            api_candidates = result["result"]
            if api_candidates:
                st.subheader(f"📌 건축물대장 후보 ({len(api_candidates)}개)")
                selected_index = st.radio(
                    "후보 선택",
                    options=range(len(api_candidates)),
                    format_func=lambda x: f"{api_candidates[x]['newPlatPlc']} - {api_candidates[x]['bldNm']} ({api_candidates[x]['dongNm']})"
                )

                candidate_details = api_candidates[selected_index]
                st.json({
                    "도로명 주소": candidate_details['newPlatPlc'],
                    "건물명": candidate_details['bldNm'],
                    "동명": candidate_details['dongNm'],
                    "주용도": candidate_details['etcPurps'],
                    "구조": candidate_details['strctCdNm'],
                    "면적(㎡)": candidate_details['archArea'],
                    "사용승인일": candidate_details['useAprDay'],
                    "지상층 수": candidate_details['grndFlrCnt'],
                    "지하층 수": candidate_details['ugrndFlrCnt'],
                })

                # 🔹 "매칭 확정" 및 "PASS" 버튼을 나란히 배치
                match_col, pass_col = st.columns([2, 1])

                def move_to_next():
                    """다음 물건을 자동 선택"""
                    st.session_state.selected_index = (st.session_state.selected_index + 1) % len(items_list)
                    st.rerun()

                with match_col:
                    if st.button("✅ 매칭 확정"):
                        match_type = "admin_ilban_match" if group_type == "일반건축물" else "admin_junyu_match"
                        match_payload = {
                            "request_type": match_type,
                            "i_code": i_code,
                            "jibun_code": jibun_code if group_type == "일반건축물" else None,
                            "ilban_info": candidate_details if group_type == "일반건축물" else None,
                            "junyu_info": candidate_details if group_type == "전유건축물" else None
                        }

                        match_response = requests.post(LAMBDA_URL, json=match_payload)

                        if match_response.status_code == 200:
                            st.success(f"✅ 매칭 완료: {candidate_details['newPlatPlc']} - {candidate_details['bldNm']} ({candidate_details['archArea']}㎡)")
                            move_to_next()
                        else:
                            st.error("❌ 매칭 실패: 서버 오류 발생")

                with pass_col:
                    if st.button("❌ PASS"):
                        db = Database(schema='aboutb_pro4')
                        update_query = f"UPDATE i_request SET {'ilban_pk' if group_type == '일반건축물' else 'junyu_pk'}='0' WHERE i_code={i_code}"
                        db.insert(update_query)
                        st.warning(f"🚨 PASS 완료: i_code {i_code} ({'ilban_pk' if group_type == '일반건축물' else 'junyu_pk'}=0 설정됨)")
                        move_to_next()
            else:
                st.warning("API 조회 결과 없음")
        else:
            st.error("API 호출 실패")
