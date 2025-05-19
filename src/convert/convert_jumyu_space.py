

# JSON 데이터에서 필요한 부분만 추출
data = {
    "00": "조사된 내용없음",
    "01": "주거",
    "02": "점포",
    "03": "주거및점포",
    "04": "공장",
    "09": "기타",
}


def convert(intg_cd):
    return data.get(intg_cd, "")

