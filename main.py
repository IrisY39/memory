from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# 从环境变量中读取配置
API_KEY = os.environ.get("OPENAI_API_KEY")  # 模型提供方的 API Key
BASE_URL = os.environ.get("BASE_URL")       # 例如 https://openrouter.ai/api/v1
MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-2.5-pro")  # 默认模型名称

@app.route("/")
def index():
    return "Memory Gateway is running!"

@app.route("/v1/models", methods=["GET"])
def models():
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # 请求模型提供方的 models 接口
        response = requests.get(f"{BASE_URL}/models", headers=headers)

        return (response.content, response.status_code, response.headers.items())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    try:
        incoming_data = request.json

        proxy_payload = {
            "model": incoming_data.get("model", MODEL_NAME),
            "messages": incoming_data["messages"],
            "temperature": incoming_data.get("temperature", 0.7),
            "top_p": incoming_data.get("top_p", 1),
            "n": incoming_data.get("n", 1),
            "stream": incoming_data.get("stream", False),
            "max_tokens": incoming_data.get("max_tokens", 1024),
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        upstream_url = f"{BASE_URL}/chat/completions"
        response = requests.post(upstream_url, headers=headers, json=proxy_payload)

        return (response.content, response.status_code, response.headers.items())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)