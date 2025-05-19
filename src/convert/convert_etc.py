
def case_code_change(c_num):
    YYYY= c_num[:4]
    NNNNN= c_num[6:]

    if len(NNNNN) == 6:
        c_num=YYYY+'0'+NNNNN

    elif len(NNNNN) == 5:
        c_num=YYYY+"00"+NNNNN

    elif len(NNNNN) == 4:
        c_num=YYYY+"000"+NNNNN

    elif len(NNNNN) == 3:
        c_num=YYYY+"0000"+NNNNN

    elif len(NNNNN) == 2:
        c_num=YYYY+"00000"+NNNNN

    elif len(NNNNN) == 1:
        c_num=YYYY+"000000"+NNNNN

    return c_num

def saNo_change(c_code):
    YYYY= c_code[2:6]
    NNNNN= c_code[6:]

    c_code=YYYY+'013'+NNNNN
    
    return c_code

def mul_code_change(m_num):
    if len(m_num) == 1:
        m_num = ('00'+ m_num)
    elif len(m_num) == 2:
         m_num = ('0' + m_num)
    return m_num

def mul_code_change_reverse(mul_code):
    if mul_code[0] == '0' and mul_code[1] == '0':
        m_num = mul_code[2]
    elif mul_code[0] == '0' and mul_code[1] != '0':
        m_num = mul_code[1:]
    else:
        m_num=mul_code

    return m_num

def item_code_change(item_num):
    if len(item_num) == 1:
        item_num = ('00'+ item_num)
    if len(item_num) == 2:
        item_num = ('0' + item_num)

    return item_num


def format_date(date_str):
    """
    날짜를 '0000-00-00' 형식으로 변환. 값이 없거나 길이가 맞지 않으면 '0000-00-00'을 반환.
    """
    if not date_str or len(date_str) != 8:
        return "0000-00-00"
    
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"


def juso_code_change(jibun_b_code,jibun_mountain_yn,jibun_main_address_no,jibun_sub_address_no):

    try:
        if jibun_mountain_yn == 'Y':
            item_gubun_code='1'
            item_gubun_code2='2'

        elif jibun_mountain_yn == 'N': 
            item_gubun_code='0'
            item_gubun_code2='1'
        
        if len(jibun_main_address_no) == 0:
            jibun_main_address_no = '0000'
        elif len(jibun_main_address_no) == 1:
            jibun_main_address_no= '000' +jibun_main_address_no
        elif len(jibun_main_address_no) == 2:
            jibun_main_address_no= '00' +jibun_main_address_no
        elif len(jibun_main_address_no) == 3:
            jibun_main_address_no= '0' +jibun_main_address_no
        
        if len(jibun_sub_address_no) == 0:
            jibun_sub_address_no = '0000'
        elif len(jibun_sub_address_no) == 1:
            jibun_sub_address_no= '000' +jibun_sub_address_no
        elif len(jibun_sub_address_no) == 2:
            jibun_sub_address_no= '00' +jibun_sub_address_no
        elif len(jibun_sub_address_no) == 3:
            jibun_sub_address_no= '0' +jibun_sub_address_no

        jibun_addr_code=jibun_b_code+item_gubun_code+jibun_main_address_no+jibun_sub_address_no #건축물대장
        jibun_addr_code2=jibun_b_code+item_gubun_code2+jibun_main_address_no+jibun_sub_address_no #토지이용규제
        addr_code_list = [jibun_addr_code , jibun_addr_code2]
    except Exception:
        addr_code_list=[]
    
    return addr_code_list

def class_name_to_code(item_class_name):
    if item_class_name == '토지':
        return '1'
    elif item_class_name == '건물':
        return '2'
    elif item_class_name == '집합건물':
        return '3'
    else:
        return '4'
        
def i_detail_info_change(i_detail_info):
    i_detail_info_for=i_detail_info.replace('\t','').replace('\xa0','').replace('1동의  건물의 표시 \n \n','').replace('\n\n','@').replace('\n \n','@').replace(' \n  ','@').replace('\n','@').replace('[도로명주소]','[도로명 주소]')
    try:
        if '[도로명 주소]' in i_detail_info_for:
            i_jibun_juso=i_detail_info_for.split('@')[0]
        else:
            i_jibun_juso=''
    except IndexError:
        i_jibun_juso=''
        
    return i_jibun_juso

def ex_area(i_detail_info):
    if "제시외건물" in i_detail_info:
        i_ex_area=' '.join(i_detail_info.split('제시외건물')[1].split())
        return i_ex_area
    else:
        return ''

'''리뉴얼 변환코드'''

def convert_class_code(renew_class_code):
    if renew_class_code == "01":
        class_code = "1"
    elif renew_class_code == "02":
        class_code = "2"
    elif renew_class_code == "03":
        class_code = "3"
    else:
        class_code = "4"
    return class_code

def convert_pnu(item):
    try:
        # 필수 값 추출 (값이 없거나 형식이 맞지 않으면 예외 발생)
        sd_code = item.get("rprsAdongSdCd", "").zfill(2)  # 시도코드 (2자리)
        sgg_code = item.get("rprsAdongSggCd", "").zfill(3)  # 시군구코드 (3자리)
        emd_code = item.get("rprsAdongEmdCd", "").zfill(3)  # 읍면동코드 (3자리)
        ri_code = item.get("rprsAdongRiCd", "").zfill(2)  # 리코드 (2자리)
        ltno_addr = item.get("rprsLtnoAddr", "").strip()  # 지번 (예: "산7-19" 또는 "7-19")

        # 필수 값이 비어있다면 "" 반환
        if not all([sd_code.strip(), sgg_code.strip(), emd_code.strip(), ri_code.strip(), ltno_addr]):
            return ""
        is_mountain = "산" in ltno_addr  # 산 여부 확인
        ltno_addr = ltno_addr.replace("산", "").strip()
        main_ltno, _, sub_ltno = ltno_addr.partition("-")
        # 본번과 부번이 숫자가 아닌 경우 예외 처리
        if not main_ltno.isdigit() or (sub_ltno and not sub_ltno.isdigit()):
            return ""

        main_ltno = main_ltno.zfill(4)  # 본번 4자리
        sub_ltno = sub_ltno.zfill(4) if sub_ltno else "0000"  # 부번 4자리 (없으면 0000)

        # PNU 코드 생성 (산이면 2, 아니면 1을 붙임)
        pnu_code = f"{sd_code}{sgg_code}{emd_code}{ri_code}{'2' if is_mountain else '1'}{main_ltno}{sub_ltno}"
        print(pnu_code)
        return pnu_code

    except Exception:
        return ""  # 예외 발생 시 빈 문자열 반환



def get_usage_name(usage_code):
    """
    용도 코드를 입력받아 해당 용도명을 반환하는 함수
    """
    usage_code = str(usage_code)
    print(usage_code)
    usage_mapping = {
        # 토지 (101XX)
        "10101": "전", "10102": "답", "10103": "과수원", "10104": "목장용지", "10105": "임야",
        "10106": "광천지", "10107": "염전", "10108": "대지", "10109": "공장용지", "10110": "학교용지",
        "10111": "주차장", "10112": "주유소용지", "10113": "창고용지", "10114": "도로", "10115": "철도용지",
        "10116": "제방", "10117": "하천", "10118": "구거", "10119": "유지", "10120": "양어장",
        "10121": "수도용지", "10122": "공원", "10123": "체육용지", "10124": "유원지", "10125": "종교용지",
        "10126": "사적지", "10127": "묘지", "10128": "잡종지",

        # 주거용 건물 (201XX)
        "20101": "단독주택", "20102": "다가구주택", "20103": "다중주택", "20104": "아파트",
        "20105": "연립주택", "20106": "다세대주택", "20107": "기숙사", "20108": "빌라",
        "20109": "상가주택", "20110": "오피스텔", "20111": "주상복합",

        # 상업시설 (211XX)
        "21101": "근린생활시설", "21102": "문화및집회시설", "21103": "종교시설", "21104": "판매시설",
        "21105": "운수시설", "21106": "의료시설", "21107": "교육연구시설", "21108": "노유자시설",
        "21109": "수련시설", "21110": "운동시설", "21111": "업무시설", "21112": "숙박시설",
        "21113": "위락시설", "21114": "교정및군사시설", "21115": "방송통신시설", "21116": "발전시설",
        "21117": "묘지관련시설", "21118": "관광휴게시설",

        # 공업시설 (221XX)
        "22101": "공장", "22102": "창고시설", "22103": "위험물저장및처리시설", "22104": "자동차관련시설",
        "22105": "동물및식물관련시설", "22106": "분뇨및쓰레기처리시설",

        # 복합용 건물 (231XX)
        "23101": "주/상용건물", "23102": "주/산용건물", "23103": "기타복합용건물"
    }

    return usage_mapping.get(usage_code, "기타")



def get_status_code_name(intgCd):
    # 상태코드 목록
    status_codes = {
        "044": "이송",
        "107": "기각",
        "108": "각하",
        "201": "배당종결",
        "204": "취하",
        "205": "취소",
        "099": "기타",
        "000": "미종국",
        "501": "<(재)항고>인용",
        "502": "<(재)항고>기각"
    }
    
    # 상태코드에 해당하는 이름 반환
    return status_codes.get(intgCd, "기타타")  # 존재하지 않는 상태코드는 '알 수 없음'으로 처리


# 감정평가 요항 코드
section_titles = {
    '00083001': '위치 및 주위환경',
    '00083002': '위치 및 부근의 상황',
    '00083003': '교통상황',
    '00083004': '인접 도로상태',
    '00083005': '인접 도로상태등',
    '00083006': '이용상태',
    '00083007': '이용상태 및 장래성',
    '00083008': '형태 및 이용상태',
    '00083009': '토지의 형상 및 이용상태',
    '00083010': '토지의 상황',
    '00083011': '토지이용계획 및 제한상태',
    '00083012': '도시계획 및 기타공법상의 제한사항',
    '00083013': '제시목록 외의 물건',
    '00083014': '공부와의 차이',
    '00083015': '건물의 구조',
    '00083016': '건물의 구조 및 현상',
    '00083017': '설비내역',
    '00083018': '부합물 및 종물',
    '00083019': '기계/기구의 현상',
    '00083020': '공작물의 현상',
    '00083021': '년식 및 주행거리',
    '00083022': '색상',
    '00083023': '관리상태',
    '00083024': '사용연료',
    '00083025': '유효검사기간',
    '00083026': '기타참고사항(임대관례 및 기타)',
    '00083027': '기타참고사항',
    '00083028': '기타(옵션등)',
    '00083029': '입지조건',
    '00083030': '임지사항',
    '00083031': '임목상황',
    '00083032': '사업체의 개요',
    '00083033': '어종 및 어기',
    '00083034': '어장의 시설현황',
    '00083035': '어획고 및 동변천상황과 판로',
    '00083036': '경영상황'
}