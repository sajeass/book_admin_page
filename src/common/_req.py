import requests
import json
import random
from bs4 import BeautifulSoup as BS
from urllib.parse import quote
import time
import configparser
import socket
import os

class Req(object):
    def __init__(self, url, req_type='default', request_method='get', cookies=None, use_proxy=False,referer=None, **kwargs):
        cookies = cookies or {}
        self.url = url
        self.req_type = req_type
        self.request_method = request_method
        self.cookies = cookies
        self.use_proxy = use_proxy
        self.referer = referer
        self.timeout = 60
        self.proxies = self.default_proxies() if use_proxy else None

        self.payload = kwargs.get('payload', {})
        # ✅ `kwargs`의 모든 키-값을 `payload`에 자동 추가 (중복 키는 유지)
        for key, value in kwargs.items():
            if key != "payload":  # 기존 `payload` 값 제외
                self.payload[key] = value
                
        # Load configuration
        self.config = self.load_config()

        # Set headers and user-agent list
        self.user_agent_list = self.generate_user_agent_list()
        self.headers = self.generate_headers(req_type)

        # Add payload based on request type
        self.configure_payload()

        self.req = None
        
    def load_config(self):
        config = configparser.ConfigParser(interpolation=None)
        root_path = os.getcwd()
        hostname = socket.gethostname()

        if hostname == 'shu2032':
            config_path = r'C:\\Users\\sajea\\OneDrive\\\uBB38\uC11C\\GitHub\\crawler_webserver\\config.ini'
        elif hostname == 'DESKTOP-77JGH89':
            config_path = r'C:\\Users\\songsong\\OneDrive - \uC544\uBC14\uC6B0\uBE44\\\uBB38\uC11C\\GitHub\\crawler_webserver\\config.ini'
        elif hostname == 'HJui-MacBookAir.local':
            root_path = os.getcwd()
            config_path = os.path.join(root_path, "config.ini")
        else:
            config_path = f"{root_path}/config.ini"

        
        config.read(config_path)
        return config

    def generate_user_agent_list(self):
        return [
            'Mozila/5.0 (Linux; Android 10; SM-F700N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.81 Mobile Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4243.0 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
            # Original user agents can be added here...
        ]

    def generate_headers(self, req_type):
        if req_type == 'daum':
            return {
                'Host': 'auction.realestate.daum.net',
                'Connection': 'keep-alive',
                'User-Agent': random.choice(self.user_agent_list),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
            }
        elif req_type == 'kakao':
            api_key = quote(self.config['production']['KAKAO_API_KEY'])
            return {'Authorization': f'KakaoAK {api_key}'}
        elif req_type == 'daum_code':
            return {'referer': self.url, 'User-Agent': random.choice(self.user_agent_list)}
        
        elif req_type == 'renew_court':
            
            return {
            "User-Agent": random.choice(self.user_agent_list),
            "Accept": "application/json",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://www.courtauction.go.kr",
            "Referer": "https://www.courtauction.go.kr/pgj/index.on?w2xPath=/pgj/ui/pgj100/PGJ151F00.xml",
            "Connection": "keep-alive",
            "sc-pgmid": "PGJ15BM01",
            "sc-userid": "NONUSER",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }
        
        elif req_type == 'portal_scourt':
            return {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=UTF-8",
            "DNT": "1",
            "Host": "ecfs.scourt.go.kr",
            "Origin": "https://ecfs.scourt.go.kr",
            "Referer": "https://ecfs.scourt.go.kr/psp/index.on",
            "SC-TraceId": "undefined@sajeas1",
            "SC-Userid": "sajeas1",
            "SC-Pgmid": "SGVO201",
            "SC-Token": "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..dDpObXu_r2UcGXwWrI0Wgg.3YxuxmW4z0ETZchVD_vA5VGDEfx56e1yW7S_YGHbw5L5nKi9nUePg1tYVcRSLNdzFUeHFSByRLYihl7EARWnD6ZlujCSogOE2IUZ8bsyhr4dV8njSSC6DmJB8DneQQdGd_f-zivUwILyQPCwledPMV6QvUechb3wpeJ3L1lSNth-pJeuASdBhT141-WzP82OG9AblkKUJCroeYSxOOEft8yJtUQAPUdMwudybGZhnPInuz4wgKGFG3JWkZ91oWn8.zVc0YKHEvG06FpNmziUtyg",  # 토큰을 헤더에도 포함
            "Sec-Ch-Ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "SubmissionId": "mf_pmf_content1_sbm_searchDlvrDocCnt",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        }

        elif req_type == 'eval':
            return {'referer': self.referer or self.url,
                    'host':'ca.kapanet.or.kr',
                    'Accept-Encoding': 'gzip, deflate',
                    # "Accept-Charset": "utf-8",
                    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'DNT': '1',
                    'User-Agent': random.choice(self.user_agent_list),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    
                    }
        
        elif req_type == 'seum':
            return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "DNT": "1",
        "Host": "www.eais.go.kr",
        "Origin": "https://www.eais.go.kr",
        "Referer": "https://www.eais.go.kr/moct/bci/aaa02/BCIAAA02L01",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "UntClsfCd": "1000",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Cookie": "TMOSHCooKie=AdGh5dJjT1u5RJB1SJEzV+Ey2qDyCO7jJX39a1UVJ1/4sGdQ+h7Yj1BIy6uvc/MziBbEvSrQWv9RI2W4gcRmO5KtZjL0G6gAAAAB; WHATAP=x4f5qm77sif47f; membIdSave=sajeas2; SESSION=ZjdiY2E5MDYtODUyZC00N2YyLThiMzYtZTdiMTMzNWRiNzYw; clientid=000033515490; TMOSHCooKie=fAOuutAftlNUpj91SJEzV+Ey2qDyCLMBbusc2CxIkY1241d9oUZcW1ZcsW6XL9D/29bDNl6oSzc17oS/IMcMn0KCiT/0STAAAAAB; JSESSIONID=Vl201NPJ4i2lWN-bs_t1D3N492GJrLvNnFAobsqz.ms-gateway"
    }   
        
        elif req_type == 'blcm':
            return {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "JSESSIONID=UNlzaLl9lsHYCO55jhvz54tPaIM86NXUAJi40yQSubhGKD9xvka9lo1muGNcY7cG.amV1c19kb21haW4vb3BlbmFwaTI=",
    "DNT": "1",
    "Host": "blcm.go.kr",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"'
}

        else:
            return {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        
    def configure_payload(self):
        if self.req_type == 'court_case':
            self.payload['_SRCH_SRNID'] = 'PNO102014'
        elif self.req_type == 'court_collect':
            self.payload['page'] = 'default50'
            self.payload['pageSpec'] = 'default40'
        elif self.req_type == 'book':
            MYAPP_KEY = quote(self.config['production']['DATA_API_KEY'])
            self.payload['ServiceKey'] = MYAPP_KEY
        elif self.req_type == 'public_data_api':
            MYAPP_KEY = self.config['production']['DATA_API_KEY']
            self.payload['serviceKey'] = MYAPP_KEY
        elif self.req_type == 'public_data_vworld':
            MYAPP_KEY = quote(self.config['production']['VWORLD_API_KEY'])
            self.payload['key'] = MYAPP_KEY
            self.payload['domain'] = 'madangs.com'

    def default_proxies(self):
        proxy_host = "geo.iproyal.com"
        proxy_port = "12321"
        proxy_username = "qxBkVs61Hwm579Rk"
        proxy_password = "0ol00ToKxDbJXq04_country-kr_streaming-1"
        return {
            "http": f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
            "https": f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
        }

        # proxy_host = "portal.anyip.io"
        # proxy_port = "1080"
        # proxy_username = "user_97a1e1,type_residential"
        # proxy_password = "48e41b"
        # return {
        #     "http": f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
        #     "https": f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
        # }
        
    def request(self):
        try:

            if self.request_method == 'get':
                self.req = requests.get(
                    self.url, params=self.payload,allow_redirects=True, headers=self.headers, cookies=self.cookies, proxies=self.proxies, timeout=self.timeout
                    )
                # print(f"Request get: {self.req.url}")  # payload가 포함된 경우 확인
                
            elif self.request_method == 'post':
                self.headers['Content-Type'] = 'application/json'
                self.req = requests.post(
                    self.url, json=self.payload, allow_redirects=True, headers=self.headers, cookies=self.cookies, proxies=self.proxies, timeout=self.timeout
                )
                print(f"Request Payload: {self.url} {self.payload}")  # payload가 포함된 경우 확인
                # print(self.req.status_code)
                # print(self.req.text)
                
        except requests.RequestException as e:
            print(f"Request URL: {self.url,self.payload}")
            print(f"Request error: {e}")


    def html_test(self):
        if not self.req or self.req.status_code != 200:
            return False

        html = BS(self.req.text, 'html.parser')

        if self.req_type.startswith('court'):
            if html.select("div[id*='wrong_ac']") or html.select("div[id*='wrong_gd']"):
                return False
            elif html.select("img[src*='/images/info_nopage.gif']"):
                return False
            return True

        if self.req_type == 'items_extra':
            table_row = html.select_one("table[summary*='\uBAA9\uB85D\uB0B4\uC5ED \uD45C'] > tbody > tr")
            if table_row and table_row.text.strip() == '\uAC80\uC0C9\uACB0\uACFC\uAC00 \uC5C6\uC2B5\uB2C8\uB2E4.':
                return False
            return True

        if self.req_type.startswith('daum'):
            if '비정상적인 접속 아이피' in (html.select_one("#docDaum").text if html.select_one("#docDaum") else ''):
                print('다음 ip ban')
                return False
            if not html.select_one("input[name='chkone[]']"):
                print('다음 페이지 오류')
                return False
            return True

        return True

    def html(self):
        self.request()
        if self.html_test():
            return BS(self.req.text, 'html.parser')
        return None

    def json(self):
        self.request()
        if self.req and self.req.status_code == 200:
            try:
                return self.req.json()
            except json.JSONDecodeError:
                print("JSON decode error")
        return None

    def xml(self):
        self.request()
        return BS(self.req.text, 'html.parser')

    def contents_test(self):
        if self.req:
            if self.req.status_code == 200:
                return True
            else:
                return False

    def contents(self):
        self.request()
        if self.contents_test():
            return self.req.content
        else:
            return None

    def cookie(self):
        self.request()
        if self.req and self.req.status_code == 200:
            return self.req.cookies
        return None