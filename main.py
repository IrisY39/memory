from flask import Flask, request, jsonify, Response
import os, requests, json

app = Flask(__name__)

API_KEY    = os.environ["OPENAI_API_KEY"]        # 必填
BASE_URL   = os.environ["BASE_URL"]              # 必填，如 https://openrouter.ai/api/v1
MODEL_NAME = os.environ["MODEL_NAME"]            # 必填，如 gemini-2.5-pro

@app.route("/")
def index():
    return "Memory Gateway is running!"

# 让 Chatbox 成功拉模型
@app.route("/v1/models", methods=["GET"])
def list_models():
    return jsonify({
        "object": "list",
        "data": [{
            "id": MODEL_NAME,
            "object": "model",
            "created": 1677858242,
            "owned_by": "memory-gateway"
        }]
    })

# 转发聊天
@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    try:
        payload = request.get_json(force=True)

        # 若前端没带 model，就补上你想用的
        payload["model"] = payload.get("model", MODEL_NAME)

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type":  "application/json"
        }

        upstream_resp = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )

        # 打印到日志便于调试
        print("⇡ upstream status:", upstream_resp.status_code)
        print("⇡ upstream body:",   upstream_resp.text[:400])

        # 直接把 JSON / bytes 回传给 Chatbox
        return Response(
            upstream_resp.content,
            status = upstream_resp.status_code,
            content_type = upstream_resp.headers.get("Content-Type", "application/json")
        )

    except Exception as e:
        print("❌ gateway error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)