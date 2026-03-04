import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# 解决某些环境下的编码显示问题
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

# 详细配置 CORS，允许所有来源和常用的 Content-Type
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# 建议在 Render 的 Environment Variables 中设置 DEEPSEEK_API_KEY
# 如果没设置，则回退到你提供的这个 Key（注意：公开代码中泄露 Key 有风险）
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "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")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = """
你是一名拥有10万粉丝的科技公众号主编。
人设特征：长期关注智能硬件、汽车电子、海外市场；说话锐利但不油腻；有项目经理思维；善于用通俗表达讲清复杂问题；偶尔幽默；句子短；像真人聊天；不要AI腔。

输出要求：
1）给出3个标题：悬念型、利益型、专业型
2）正文结构：【引言】【核心内容】分段+小标题【主编点评】
3）最后输出2条英文图像Prompt：
Image 1: cyberpunk or minimal tech style
Image 2: explain core concept visually
"""

@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    # 处理浏览器的预检请求 (Options)
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        data = request.json
        if not data or "content" not in data:
            return jsonify({"error": "Missing 'content' in request body"}), 400
        
        content = data.get("content")

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content}
            ],
            temperature=0.85
        )

        return jsonify({"result": response.choices[0].message.content})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render 部署的关键：监听 0.0.0.0 并读取环境变量中的 PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)