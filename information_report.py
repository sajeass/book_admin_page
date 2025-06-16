import streamlit as st
import smtplib
from email.message import EmailMessage

st.title("물건 정보 제보")

# 법원명 리스트
court_names = [
    "서울중앙지방법원", "서울동부지방법원", "서울서부지방법원", "서울남부지방법원", "서울북부지방법원",
    "의정부지방법원", "고양지원", "인천지방법원", "부천지원", "수원지방법원",
    "성남지원", "여주지원", "평택지원", "안산지원", "안양지원",
    "춘천지방법원", "강릉지원", "원주지원", "속초지원", "영월지원",
    "청주지방법원", "충주지원", "제천지원", "영동지원",
    "대전지방법원", "홍성지원", "논산지원", "천안지원", "공주지원", "서산지원",
    "대구지방법원", "안동지원", "경주지원", "김천지원", "상주지원", "의성지원", "영덕지원", "포항지원", "대구서부지원",
    "부산지방법원", "부산동부지원", "부산서부지원",
    "울산지방법원", "창원지방법원", "마산지원", "진주지원", "통영지원", "밀양지원", "거창지원",
    "광주지방법원", "목포지원", "장흥지원", "순천지원", "해남지원",
    "전주지방법원", "군산지원", "정읍지원", "남원지원",
    "제주지방법원", "남양주지원"
]

# 채권자명 고정 출력
st.markdown("채권자명")
st.text_input(" ", value="대구신협", disabled=True, label_visibility="collapsed")

# 1. 법원 선택
court_name = st.selectbox("법원 선택 (예: 서울중앙지방법원)", court_names)

# 2. 사건년도 (역순)
years = list(range(2025, 1999, -1))
year = st.selectbox("사건년도 (예: 2025)", years)

# 3. 사건번호 입력
event_number = st.text_input("사건번호 (숫자만 입력, 예: 123456)", max_chars=6)

# 4. 물건번호
item_number = st.selectbox("물건번호 (예: 1)", list(range(1, 101)))

# 설명 입력
text_data = st.text_area("내용 입력 (자유롭게 입력해주세요)")

# 이미지 업로드
uploaded_images = st.file_uploader("이미지 업로드 (JPG, PNG - 여러 개 가능)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# 파일 업로드
uploaded_files = st.file_uploader("첨부 파일 업로드 (PDF, DOC, XLSX 등 - 여러 개 가능)", type=["pdf", "doc", "docx", "xls", "xlsx"], accept_multiple_files=True)

# 제출 버튼
if st.button("제출하기"):
    if not event_number.strip():
        st.warning("사건번호를 입력해주세요.")
    else:
        # 사건번호 전체 조합
        full_case_code = f"{court_name} {year}타경{event_number.zfill(6)} {str(item_number).zfill(3)}"

        # 이메일 메시지 구성
        msg = EmailMessage()
        msg['Subject'] = f"[채권자 제보] {full_case_code}"
        msg['From'] = "we-seed@we-seed.net"  # 보내는 사람
        msg['To'] = "we-seed@we-seed.net"  # 받는 사람
        msg.set_content(f"""\
📌 사건번호: {full_case_code}

📝 설명:
{text_data}
""")

        # 이미지 첨부
        for img in uploaded_images:
            msg.add_attachment(
                img.read(),
                maintype="image",
                subtype=img.type.split("/")[-1],
                filename=img.name
            )

        # 파일 첨부
        for file in uploaded_files:
            msg.add_attachment(
                file.read(),
                maintype="application",
                subtype="octet-stream",
                filename=file.name
            )

        # 이메일 전송
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login("we-seed@we-seed.net", "qbqtfstdxcditbca")
                smtp.send_message(msg)
            st.success("제보가 이메일로 전송되었습니다. 감사합니다!")
        except Exception as e:
            st.error(f"이메일 전송 실패: {e}")
