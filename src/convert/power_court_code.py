# 새로운 코드(new_code)를 기존 코드(old_code)로 변환하여 반환하는 함수
def convert_power_to_jiwon_code(power_code):
    data_map = {
        "A01": "01",
        "A02": "02",
        "A03": "03",
        "A04": "04",
        "A05": "05",
        "B01": "40",
        "B02": "41",
        "B03": "42",
        "C01": "08",
        "C02": "09",
        "D01": "06",
        "D02": "07",
        "D03": "61",
        "E01": "10",
        "E02": "11",
        "E03": "12",
        "E04": "13",
        "E05": "14",
        "E06": "15",
        "F01": "16",
        "F02": "17",
        "F03": "19",
        "F04": "18",
        "F05": "20",
        "G01": "21",
        "G02": "22",
        "G03": "23",
        "G04": "24",
        "H01": "25",
        "H02": "28",
        "H03": "29",
        "H04": "30",
        "H05": "26",
        "H06": "27",
        "I01": "31",
        "I02": "33",
        "I03": "34",
        "I04": "35",
        "I05": "32",
        "I06": "37",
        "I07": "36",
        "I08": "38",
        "I09": "39",
        "J01": "44",
        "J02": "49",
        "J03": "48",
        "J04": "46",
        "J05": "47",
        "J06": "45",
        "K01": "55",
        "K02": "56",
        "K03": "58",
        "K04": "57",
        "L01": "50",
        "L02": "53",
        "L03": "51",
        "L04": "52",
        "L05": "54",
        "M01": "59",
        "N01": "43"
    }

    jiwon_code = data_map.get(power_code,"")
    return jiwon_code


