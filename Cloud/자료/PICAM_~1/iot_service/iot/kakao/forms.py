from django import forms
import json
import requests

class KaKaoTalkForm(forms.Form):
    text = forms.CharField(label='전송할 Talk', max_length=300)
    web_url = forms.CharField(label='Web URL', max_length=300, initial='http://192.168.25.14:8000/mjpeg?mode=stream')
    mobile_web_url = forms.CharField(label='Mobile Url', max_length =300, initial='http://192.168.25.14:8000/mjpeg?mode=stream')
    #중요 스마트폰 이용시 이것 저것슨
    #(views에서 send_talk 이러한 기본적인 form을 통과했을 경우 views.py 에서 def form_valid가 실행됩니다.)

    def send_talk(self):
        talk_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        with open("access_token.txt", "r") as f:
            token = f.read() #이 토큰은 발행 이후 6시간의 유효시간을 가짐 유효시간이 지난다면 다시 로그인 후 진행 해야함
        header = {"Authorization": f"Bearer {token}"}
        #전송한 데이터의 전체적인 구성형태를 지정스
        text_template = {
            "object_type": "feed",
            "content": {
            "title": "디저트 사진",
            "description": "아메리카노, 빵, 케익",
            "image_url": "http://mudkage.kakao.co.kr/dn/NTmhS/btqfEUdFAUf/FjKzkZsnoeE4o19klTOVI1/openlink_640x640s.jpg",
            "image_width": 640,
            "image_height": 640,
            "link": {
                "web_url": "http://www.daum.net",
                "mobile_web_url": "http://m.daum.net",
                "android_execution_params": "contentId=100",
                "ios_execution_params": "contentId=100"
            }},
"social": {
"like_count": 100,
"comment_count": 200,
"shared_count": 300,
"view_count": 400,
"subscriber_count": 500
},
"buttons": [
{
"title": "웹으로 이동",
"link": {
"web_url": "http://www.daum.net",
"mobile_web_url": "http://m.daum.net"
}
},
{
"title": "앱으로 이동",
"link": {
"android_execution_params": "contentId=100",
"ios_execution_params": "contentId=100"
}
}
]

            # 'object_type': 'text',
            # 'text': self.cleaned_data['text'],
            # 'link': {
            #     'web_url': self.cleaned_data['web_url'],
            #     'mobile_web_url': self.cleaned_data['mobile_web_url']
            # },
            # 'button_title' : '카메라 보기'
        }
        print(text_template)
        payload = {'template_object': json.dumps(text_template)}
        res = requests.post(talk_url, data=payload, headers=header)

        return res, self.cleaned_data['text'] #응답한 것(response)과 실제 사용자가 입력한 텍스트를 리턴

    #매우 중요하며, 다른 프로그램에서도 (kakao 와 연동시 써먹을 수 있는 중요한) 코드입니다.
    #텍스트 하나와 링크 하나만 보내는 중