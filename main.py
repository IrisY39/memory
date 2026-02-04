from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Memory Gateway is running!"

@app.route("/chat/completions", methods=["POST"])
def completions():
    data = request.json
    messages = data.get("messages", [])
    
    # 简单回显最后一条用户消息
    user_message = ""
    for message in reversed(messages):
        if message.get("role") == "user":
            user_message = message.get("content", "")
            break

    reply = f"你刚才说的是：{user_message}"

    return jsonify({
        "id": "chatcmpl-mockid",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "gpt-4",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": reply
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  
    app.run(host="0.0.0.0", port=port)