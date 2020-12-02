from flask import Flask, render_template           # 플라스크 모듈 호출

app = Flask(__name__)               # 플라스크 앱 생성        

@app.route('/')                     # 기본('/') 웹주소로 요청이 오면                     
def hello():                        # hello 함수 실행
    return 'Hello world'

@app.route('/camera/<username>')
def camera(username):
    return render_template('index.html', user=username)

if __name__ == '__main__':          # 현재 파일 실행시 개발용 웹서버 구동
    app.run(debug=True, port=80, host='0.0.0.0')     