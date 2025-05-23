import json

# JSON 데이터 (전체 데이터 포함)
data = {
    "가단": "001",
    "가합": "002",
    "가소": "003",
    "나": "004",
    "다": "005",
    "다카": "006",
    "라": "007",
    "카": "008",
    "마": "009",
    "바": "010",
    "자": "011",
    "차": "012",
    "타경": "013",
    "타기": "014",
    "파": "015",
    "호파": "016",
    "하": "017",
    "거": "018",
    "더": "019",
    "러": "020",
    "머": "021",
    "느": "022",
    "드": "023",
    "르": "024",
    "므": "025",
    "브": "026",
    "스": "027",
    "즈": "028",
    "너": "029",
    "츠": "030",
    "프": "031",
    "흐": "032",
    "구": "033",
    "누": "034",
    "두": "035",
    "루": "036",
    "부": "037",
    "수": "038",
    "슈": "039",
    "재수": "040",
    "주": "041",
    "쥬": "042",
    "추": "043",
    "쿠": "044",
    "재추": "045",
    "후": "046",
    "재후": "047",
    "그": "048",
    "마카": "049",
    "재가단": "050",
    "재가합": "051",
    "재가소": "052",
    "재나": "053",
    "재다": "054",
    "재다카": "055",
    "재구": "056",
    "재누": "057",
    "재차": "058",
    "재드": "059",
    "재르": "060",
    "재므": "061",
    "우": "062",
    "재우": "063",
    "재머": "064",
    "각하": "065",
    "준재가단": "066",
    "준재가합": "067",
    "준재가소": "068",
    "카공": "069",
    "집제": "070",
    "카합": "071",
    "카단": "072",
    "카담": "073",
    "카기": "074",
    "고합": "075",
    "감고": "076",
    "고단": "077",
    "고약": "078",
    "노": "079",
    "감노": "080",
    "도": "081",
    "감도": "082",
    "로": "083",
    "감로": "084",
    "모": "085",
    "감모": "086",
    "보": "087",
    "오": "088",
    "감오": "089",
    "조": "090",
    "초": "091",
    "감초": "092",
    "코": "093",
    "토": "094",
    "감토": "095",
    "투": "096",
    "수호": "097",
    "푸": "098",
    "크": "099",
    "정": "100",
    "정로": "101",
    "정초": "102",
    "정모": "103",
    "보증": "104",
    "준재나": "105",
    "준재머": "106",
    "호": "107",
    "호과": "108",
    "수흐": "109",
    "으": "110",
    "트": "111",
    "재고합": "112",
    "재고단": "113",
    "재고약": "114",
    "재노": "115",
    "재도": "116",
    "재감고": "117",
    "재감노": "118",
    "재감도": "119",
    "타": "120",
    "급여": "121",
    "재타경": "122",
    "재마": "123",
    "재그": "124",
    "준재자": "125",
    "사": "126",
    "아": "127",
    "재두": "128",
    "허": "129",
    "히": "130",
    "카허": "131",
    "재허": "132",
    "무": "133",
    "재자": "134",
    "버": "135",
    "서": "136",
    "어": "137",
    "저": "138",
    "재아": "139",
    "준재구": "140",
    "준재누": "141",
    "준재아": "142",
    "준재드": "143",
    "준재르": "144",
    "준재므": "145",
    "재브": "146",
    "재스": "147",
    "준재브": "148",
    "준재스": "149",
    "드단": "150",
    "드합": "151",
    "재드단": "152",
    "재드합": "153",
    "준재드단": "154",
    "준재드합": "155",
    "너단": "156",
    "너합": "157",
    "재너단": "158",
    "재너합": "159",
    "준재너단": "160",
    "준재너합": "161",
    "느단": "162",
    "느합": "163",
    "재느단": "164",
    "재느합": "165",
    "준재느단": "166",
    "준재느합": "167",
    "재라": "168",
    "준재두": "169",
    "준재다": "170",
    "금": "171",
    "증": "172",
    "물": "173",
    "준재라": "174",
    "재하": "175",
    "준재하": "176",
    "즈단": "177",
    "즈합": "178",
    "과": "179",
    "회": "180",
    "선": "181",
    "유": "182",
    "재너": "183",
    "재무": "184",
    "준재타경": "185",
    "준재루": "186",
    "푸초": "187",
    "재루": "188",
    "재카합": "189",
    "재카단": "190",
    "재카담": "191",
    "재카기": "192",
    "영장": "193",
    "구단": "194",
    "구합": "195",
    "재구단": "196",
    "재구합": "197",
    "준재구단": "198",
    "준재구합": "199",
    "타채": "200",
    "카명": "201",
    "화": "202",
    "책": "203",
    "초적": "204",
    "초보": "205",
    "초기": "206",
    "파합": "207",
    "파단": "208",
    "하합": "209",
    "하단": "210",
    "즈기": "211",
    "카조": "212",
    "카구": "213",
    "하면": "214",
    "비합": "215",
    "비단": "216",
    "재카구": "217",
    "재과": "218",
    "준재카합": "219",
    "준재카단": "220",
    "준재카담": "221",
    "준재카기": "222",
    "준재과": "223",
    "재타기": "224",
    "재즈단": "225",
    "재즈합": "226",
    "재하단": "227",
    "재하면": "228",
    "재타채": "229",
    "고정": "230",
    "재고정": "231",
    "공영": "232",
    "재어": "233",
    "고약전": "234",
    "초사": "235",
    "카불": "236",
    "정과": "237",
    "정러": "238",
    "정머": "239",
    "정가": "240",
    "정명": "241",
    "정라": "242",
    "정마": "243",
    "정고": "244",
    "정드": "245",
    "정브": "246",
    "정스": "247",
    "정기": "248",
    "재즈기": "251",
    "준재즈기": "252",
    "개회": "253",
    "개확": "254",
    "개보": "255",
    "하보": "256",
    "화보": "257",
    "회보": "258",
    "버집": "259",
    "성": "260",
    "성로": "261",
    "성모": "262",
    "성초": "263",
    "전로": "264",
    "전고": "265",
    "전노": "266",
    "전도": "267",
    "전오": "268",
    "전초": "269",
    "전모": "270",
    "재비합": "271",
    "재비단": "272",
    "재흐": "275",
    "재정가": "280",
    "재정마": "283",
    "개기": "290",
    "회단": "291",
    "회합": "292",
    "회확": "293",
    "회기": "294",
    "하확": "295",
    "하기": "296",
    "국승": "297",
    "국지": "298",
    "타인": "300",
    "타배": "301",
    "간회단": "302",
    "간회합": "303",
    "재으": "310",
    "재부": "311",
    "행심": "320",
    "정국": "321",
    "정루": "322",
    "정무": "323",
    "정관": "324",
    "정르": "325",
    "정므": "326",
    "정지": "327",
    "정리": "328",
    "정미": "329",
    "부가": "330",
    "재카허": "331",
    "지원": "340",
    "시험": "341",
    "용역": "342",
    "동고": "350",
    "동노": "351",
    "동도": "352",
    "동오": "353",
    "동초": "354",
    "치고": "360",
    "치노": "361",
    "치도": "362",
    "치오": "363",
    "치초": "364",
    "초치": "365",
    "치로": "366",
    "치모": "367",
    "재전고": "371",
    "재전노": "372",
    "재전도": "373",
    "재버": "374",
    "재서": "375",
    "재초재": "376",
    "보고": "380",
    "보노": "381",
    "보도": "382",
    "보오": "383",
    "보초": "384",
    "보로": "385",
    "보모": "386",
    "재보고": "387",
    "재보노": "388",
    "재보도": "389",
    "디": "900",
    "미상": "901",
    "민공": "902",
    "민상": "903",
    "민신": "904",
    "민신항": "905",
    "민재": "906",
    "민재항": "907",
    "민항": "908",
    "비상": "909",
    "소": "910",
    "재신": "911",
    "지선": "912",
    "카키": "913",
    "특재": "914",
    "행상": "915",
    "행신": "916",
    "행재": "917",
    "행항": "918",
    "형비상": "919",
    "형상": "920",
    "형신": "921",
    "형재": "922",
    "형재항": "923",
    "형항": "924",
    "민": "926",
    "민합": "931",
    "공": "935",
    "독": "938",
    "재주": "940",
    "인조": "957",
    "차조": "958",
    "소조": "960",
    "민집": "967",
    "전조": "969",
    "민단": "970",
    "고": "980",
    "재고": "981",
    "민제": "990",
    "우표": "999"


}

def convert(name):
    return data.get(name, "")

