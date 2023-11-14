from flask import Flask, render_template, request, redirect, url_for, session
import openai

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 안전한 장소에서 관리해야 하는 시크릿 키를 설정하세요.

openai.api_key = ''  # 실제 API 키를 여기에 입력하세요.

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'messages' not in session:
        session['messages'] = []  # 메시지 리스트 초기화

    if request.method == 'POST':
        user_message = request.form['prompt']
        session['messages'].append(('You: ' + user_message, 'user'))  # 사용자 메시지 저장
        
        # AI 응답 구현
        ai_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="다음은 친근하고 조언을 주는 스타일로 답변해주세요: " + user_message,
            max_tokens=500
        )
        session['messages'].append(('여친: ' + ai_response.choices[0].text.strip(), 'ai'))  # AI 응답 저장
        session.modified = True  # 세션 변경 사항을 알림
        return redirect(url_for('index'))  # POST 요청 후 페이지 리디렉션으로 채팅 흐름 유지

    return render_template('index.html', messages=session['messages'])  # 채팅 메시지와 함께 템플릿 렌더링

if __name__ == '__main__':
    app.run(debug=True)  # 개발 중에는 디버그 모드를 활성화하고, 배포 시에는 비활성화하세요.
