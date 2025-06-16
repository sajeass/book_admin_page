import streamlit as st
import requests
from src.common._database import Database
import src.convert.convert_jiwon as ConvertJiwon
import src.convert.convert_etc as ConvertEtc

crawler_lambda_url = "https://3bljfdmys2jwtyhdq3i74i32ne0yadtn.lambda-url.ap-northeast-2.on.aws/crawling_new_progress"

st.set_page_config(page_title="간이 관리자", layout="centered")
st.title("🔧 간이 관리자 페이지")

if "db" not in st.session_state:
    st.session_state.db = Database(schema="aboutb_pro4")

def collect_one(db, jiwon_name, c_num, mul_num):
    jiwon_code = ConvertJiwon.convert_jiwon_code(jiwon_name, "jiwon_code")
    case_year = c_num[:4]
    case_num = c_num[6:]
    c_code = jiwon_code + ConvertEtc.case_code_change(c_num)
    mul_num = mul_num.zfill(3)
    m_code = c_code + mul_num

    st.write(f"✅ 변환 결과: jiwon_code={jiwon_code}, c_code={c_code}, m_code={m_code}")

    st.session_state.db.insert("INSERT IGNORE INTO c_basic (c_code) VALUES (%s)", (c_code,))

    return c_code

# ✅ 입력 폼
with st.form("insert_form"):
    jiwon_name = st.text_input("법원명 (예: 안산지원)", "")
    c_num = st.text_input("사건번호 (예: 2023타경1213)", "")
    mul_num = st.text_input("물건번호 (예: 1)", "")


    submitted = st.form_submit_button("처리 시작")

    if submitted:
        if not all([jiwon_name, c_num, mul_num]):
            st.error("❌ 모든 값을 입력해 주세요.")
        else:
            try:
                # ✅ 구분에 따른 progress_type 및 request_type 결정
                lambda_request_type = "crawler"
                update_type = "new"

                c_code = collect_one(st.session_state.db, jiwon_name, c_num, mul_num)

                # ✅ 1차 성공 메시지
                st.info("✅ 사건번호 DB 삽입 성공 / 크롤링 API 작업중 (10초 내외 소요)")

                # ✅ Lambda 호출 (GET 방식)
                response = requests.get(
                    crawler_lambda_url,
                    params={"request_type": lambda_request_type,"update_type":update_type, "c_code": c_code}
                )

                # ✅ 응답 처리
                if response.status_code == 200:
                    try:
                        res_json = response.json()
                        if res_json is True:
                            st.success("✅ Lambda 호출 성공: True")
                        elif isinstance(res_json, dict) and res_json.get("result") == "success":
                            st.success(f"✅ Lambda 호출 성공: {res_json}")
                        else:
                            st.error(f"❌ Lambda 처리 실패 또는 비정상 응답: {res_json}")
                    except Exception:
                        st.error(f"❌ 응답 파싱 실패 또는 비정상 응답 형식: {response.text}")
                else:
                    st.error(f"❌ Lambda 호출 실패: {response.status_code} - {response.text}")

            except Exception as e:
                st.exception(e)

# ✅ 1차 성공 메시지
st.info("✅ 사건번호 DB 삽입 성공 / 크롤링 API 작업중 (10초 내외 소요)")

# ✅ 물건 확인 링크 버튼
# st.markdown(
#     f'<a href="https://madangs.com/caview?m_code={c_code + mul_num.zfill(3)}" target="_blank">'
#     f'<button style="padding:10px 20px;font-size:16px;">🔍 웹사이트에서 물건 확인하기</button></a>',
#     unsafe_allow_html=True
# )
