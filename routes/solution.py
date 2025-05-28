# solution.py
'''
import os
import openai
from flask import Blueprint, request, jsonify, current_app
from models import ChatSolution
from db import db

solution_bp = Blueprint('solution', __name__, url_prefix='/solution')

# Flask 설정에서 OPENAI_API_KEY를 읽어오게 해두세요.
# 예: app.config['OPENAI_API_KEY'] = 'sk-...'
@solution_bp.before_app_first_request
def setup_openai():
    openai.api_key = current_app.config.get('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY')

@solution_bp.route('/ask', methods=['POST'])
def ask_solution():
    data    = request.get_json()
    user_id = data.get('user_id')
    prompt  = data.get('prompt')
    if not user_id or not prompt:
        return jsonify({'error': 'user_id와 prompt 모두 필요'}), 400

    # ChatGPT API 호출
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 반려동물 케어 전문가입니다."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        answer = resp.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({'error': 'AI 호출 실패', 'detail': str(e)}), 500

    # DB 저장
    sol = ChatSolution(user_id=user_id, prompt=prompt, answer=answer)
    db.session.add(sol)
    db.session.commit()

    return jsonify({
        'solution_id': sol.id,
        'answer': answer
    }), 200


error : File "C:\Users\mkh\flask-nmc\routes\solution.py", line 12, in <module>
    @solution_bp.before_app_first_request
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
'''