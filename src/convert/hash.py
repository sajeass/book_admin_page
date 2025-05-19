import hashlib

def generate_md5_hash(input_string):
    """
    주어진 문자열의 MD5 해시를 생성합니다.
    
    Args:
        input_string (str): 해시로 변환할 문자열.
        
    Returns:
        str: MD5 해시값 (소문자 32자리).
    """
    # 문자열을 바이트로 변환
    encoded_string = input_string.encode('utf-8')
    # MD5 해시 생성
    md5_hash = hashlib.md5(encoded_string)
    # 16진수로 변환 후 반환
    return md5_hash.hexdigest()

# 테스트
input_string = '22201738000048871276651000020170502204922835'
hash_value = generate_md5_hash(input_string)
print("MD5 해시값:", hash_value)


'2e85a0e5451c4de3b793e0b5a1c02b64'