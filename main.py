from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Memory Gateway is running!"

@app.route("/memory", methods=["POST"])
def memory():
    data = request.json
    return jsonify({"received": data})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port)