import requests

def send_teams_message(target_chatroom,message):
    """
    Microsoft Teams로 메시지를 전송합니다.
    :param title: 메시지 제목 (str)
    :param content: 메시지 내용 (str)
    """
    if target_chatroom == 'general':
        chatroom_url = "https://aboutb.webhook.office.com/webhookb2/a6add533-db9a-43dd-bbe4-fad0e3c3d9a1@7068eda5-0740-4a6f-aabe-da464a7d73a9/IncomingWebhook/0994841fcd65417abb309201de66d935/4c410da4-82a2-4193-841b-2d19106be27e/V236XzsuHjPLPOJDIIKGxgQ1NaiMXMCXmG48FWTlzn5N01"
    
    elif target_chatroom == 'personal':
        chatroom_url = "https://aboutb.webhook.office.com/webhookb2/543ddd08-c331-47ad-9291-b040d74e3300@7068eda5-0740-4a6f-aabe-da464a7d73a9/IncomingWebhook/c13651e321bb4a51a078cf085b296dc2/4c410da4-82a2-4193-841b-2d19106be27e/V2Q1YKpqU1UnsYOQMWIo7ayIeSIs7Hws3EthT5_CIfFNo1"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "summary": message
    }
    response = requests.post(chatroom_url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Teams 메시지 전송 성공")
    else:
        print(f"Teams 메시지 전송 실패: {response.status_code}, {response.text}")

if __name__ == "__main__":
    # 제목과 내용 입력
    message = "message"
    send_teams_message(message)
