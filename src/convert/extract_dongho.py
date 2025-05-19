import re

# def dongnm(original_addr_list):
#     pattern = r'\([^()]*\)'  # 괄호와 그 안의 내용을 나타내는 정규표현식
#     extracted_dongnms = []
    
#     patterns = [
#         r'(\d+)동',  # 숫자+동 형태 추출
#         r'\((?:[^()]*?(\d+)동[^()]*)\)',  # 괄호 안 동명 추출
#         r'(가|나|다|라|마|바|사|아|자|차|카|타|파|하|에이|비|씨|디|이|에프|지|에이치|A|B|C|D|E|F|G|H)동', 
#         r'(가|나|다|라|마|바|사|아|자|차|카|타|파|하|에이|비|씨|디|이|에프|지|에이치|A|B|C|D|E|F|G|H)동호'
#     ]
    
#     for original_addr in original_addr_list:
#         for pattern in patterns:
#             match = re.search(pattern, original_addr)
#             if match:
#                 extracted_dongnms.append(match.group(1))
#                 break  # 첫 번째로 매칭되는 값만 저장
    
#     return extracted_dongnms



def dongnm(original_addr_list):
    extracted_dongnms = []
    
    # '동' 앞에 붙은 모든 문자(숫자, 한글, 영문 포함)를 추출하는 정규식
    patterns = [
        r'([\w가-힣]+)동',  # 모든 문자(숫자+한글+영문 포함) + '동'
        r'\((?:[^()]*?([\w가-힣]+)동[^()]*)\)'  # 괄호 안에서 '동'을 포함하는 패턴
    ]
    
    for original_addr in original_addr_list:
        for pattern in patterns:
            match = re.search(pattern, original_addr)
            if match:
                extracted_dongnms.append(match.group(1))
    
    return extracted_dongnms



def honm(original_addr_list):
    """여러 개의 주소에서 '호' 정보를 추출하는 함수"""
    pattern = r'\([^()]*\)'  # 괄호 안의 내용을 제거하는 정규표현식
    extracted_honms = []

    for original_addr in original_addr_list:
        original_addr = original_addr.strip()  # 공백 제거

        # 숫자로만 이루어진 경우 원본 문자열 그대로 추가
        if original_addr.isdigit():
            extracted_honms.append(original_addr)
            continue

        clear_original_addr = re.sub(pattern, '', original_addr)  # 괄호 제거
        results = re.findall(r'(\d+)호', clear_original_addr)  # '123호' 같은 숫자+호 찾기
        for result in results:
            extracted_honms.extend([result, result + '호'])  # '123', '123호' 둘 다 추가

    return extracted_honms


