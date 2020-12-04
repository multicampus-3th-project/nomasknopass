from django.shortcuts import render
from django.views.generic import TemplateView, FormView
import json
import requests
from django.contrib import messages
from kakao.forms import KaKaoTalkForm

client_id = "4c32d3f02599cbae640d8ffec0b4019e"

class KakaoLoginView(TemplateView):
    template_name = "kakao_login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_id"] = client_id
        return context



class KakaoAuthView(TemplateView):
    template_name = "kakao_token.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = self.request.GET['code']
        token = self.getAccessToken(code)
        context["client_id"] = client_id
        context["token"] = token
        self.save_access_token(token["access_token"])
        return context


    # 세션 코드값 code 를 이용해서 ACESS TOKEN과 REFRESH TOKEN을 발급 받음
    def getAccessToken(self, code):
        url = "https://kauth.kakao.com/oauth/token"
        payload = "grant_type=authorization_code"
        payload += "&client_id=" + client_id
        payload += "&redirect_url=https://192.168.25.14:8000/kakao/oauth&code=" + code
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        response = requests.post(url, data=payload, headers=headers)
        return response.json()

    def save_access_token(self, access_token):
        with open("access_token.txt", "w") as f:
            f.write(access_token)

class KakaoTalkView(FormView):
    form_class = KaKaoTalkForm
    template_name = "kakao_form.html"
    success_url = "/kakao/talk"

    def form_valid(self, form): #사용자가 submit을 하고 유효성 검사를 합니다. 그 유효성 검사가 끝나면 실행되는 함수
        res, text = form.send_talk()
        #[][]나 text 리다이렉트ㅡ 하고 싶어요 근데 안되니깐

        if res.json().get('result_code') == 0:
        #엑세스 시간이 초과 됐을 경우 1이 되면서 재로그인을 해야합니다.
            messages.add_message(self.request, messages.SUCCESS, "메시지 전송 성공 : " + text)
            #[][] 얘를 씁니다.(이걸 위해서... message라는 django 함수 모듈을 사용하지 : from django.contrib import messages)
        else:
            messages.add_message(self.request, messages.ERROR, "메시지 전송 실패 : " + str(res.json()))
            #실패 이유가 ERROR를 통해 송신 될 것

        return super().form_valid(form)
        #다음 절차는 success_url로 리다이렉트 합니다.

