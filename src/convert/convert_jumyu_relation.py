def convert(rltn_cd):
    data = {
        '01': '채무자(소유자)점유',
        '02': '임차인(별지)점유',
        '03': '제 3 자점유',
        '04': '채무자(소유자)점유, 임차인(별지)점유, 제 3 자점유',
        '05': '채무자(소유자)점유, 임차인(별지)점유',
        '06': '임차인(별지)점유, 제 3 자점유',
        '07': '채무자(소유자)점유, 제 3 자점유',
        '09': '미상',
        '10': '기타점유',
        '11': '채무자(소유자)점유, 임차인(별지)점유, 기타점유',
        '12': '채무자(소유자)점유, 기타점유',
        '13': '임차인(별지)점유, 기타점유'
    }
    
    return data.get(rltn_cd, "")

