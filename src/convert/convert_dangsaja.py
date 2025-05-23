
# JSON 데이터에서 필요한 부분만 추출
data = {
    "0001505": "신청인",
    "0001507": "감정인",
    "0001515": "승계인",
    "000151E": "이해관계인",
    "0001527": "채권자",
    "0001528": "채무자",
    "0001535": "제3취득자",
    "0001536": "상대방",
    "0001550": "근저당권부질권자",
    "0001551": "수계인",
    "0001556": "지역권자",
    "0001557": "소유자",
    "0001558": "채무자겸소유자",
    "000155A": "저당권부질권자",
    "000155D": "상대방겸소유자",
    "000155E": "신청인겸소유자",
    "000155F": "상대방겸소유자대리인",
    "0001560": "최고가매수신고인",
    "0001561": "차순위매수신고인",
    "0001562": "임차인",
    "0001563": "근저당권자",
    "0001564": "가압류권자",
    "0001565": "저당권자",
    "0001566": "전세권자",
    "0001567": "압류권자",
    "0001568": "공유자",
    "0001569": "가등기권자",
    "0001570": "임금채권자",
    "0001571": "교부권자",
    "0001572": "지상권자",
    "0001573": "가처분권자",
    "0001574": "배당요구권자",
    "0001575": "점유자",
    "000157A": "유치권자",
    "0001580": "주택임차권자",
    "0001581": "임차권자",
    "0001589": "집행관",
    "0001590": "최고가매수인",
    "0001591": "차순위매수인",
    "0001592": "소유자대리인",
    "0001593": "채무자겸소유자대리인",
    "0000099": "기타"
}


def convert(intg_cd):
    return data.get(intg_cd, "")

def convert_for_parties(last_two_digits):
    # 마지막 2자리가 입력값과 일치하는 키를 찾음
    for key, value in data.items():
        if key[-2:] == last_two_digits.upper():  # 대소문자 구별 없이 비교
            return value
    return "기타"  # 일치하는 값이 없으면 빈 문자열 반환