# Main Routes
from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
import os
import requests

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Show new animated home page with slideshow to all users
    return render_template('index_animated.html')

@main.route('/explore')
def explore():
    # Allow unauthenticated users to explore the platform
    return render_template('index_animated.html')

@main.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    groq_api_key = os.getenv('GROQ_API_KEY')
    if not groq_api_key:
        return jsonify({"reply": "Server configuration error: GROQ_API_KEY not set"}), 500

    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You're a bot which intuitively explains CS from 5th to 12th Grade. "
                    "You will not use emojis inappropriately and only use them in headings. "
                    "Make learning fun. You are the bot of a website called FluxTech and your job is to help students."
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=20
        )
    except requests.RequestException as e:
        return jsonify({"reply": f"Network error contacting Groq API: {e}"}), 502

    if response.status_code != 200:
        try:
            data = response.json()
        except ValueError:
            data = response.text
        return jsonify({"reply": f"Groq API error {response.status_code}: {data}"}), 502

    data = response.json()
    if "choices" not in data or not data["choices"]:
        return jsonify({"reply": f"Unexpected Groq response: {data}"}), 502

    ai_reply = data["choices"][0]["message"]["content"]
    return jsonify({"reply": ai_reply})

@main.route('/ai')
@login_required
def ai():
    return render_template('chatbot.html')
@main.route('/course-editor')
@main.route('/lesson/<int:lesson_id>')
def course_editor(lesson_id=None):
    """Interactive course editor with code execution"""
    return render_template('course_editor.html', lesson_id=lesson_id)

@main.route('/api/execute-code', methods=['POST'])
def execute_code():
    """Execute Python or JavaScript code"""
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'python')
    
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    try:
        if language == 'python':
            import subprocess
            result = subprocess.run(
                ['python', '-c', code],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout or result.stderr
            success = result.returncode == 0
        else:
            # For JavaScript, use Node.js if available
            import subprocess
            result = subprocess.run(
                ['node', '-e', code],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout or result.stderr
            success = result.returncode == 0
        
        return jsonify({
            "success": success,
            "output": output,
            "error": None if success else "Execution error"
        })
    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "output": "",
            "error": "Code execution timeout (max 5 seconds)"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "output": "",
            "error": str(e)
        })