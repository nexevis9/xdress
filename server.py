from flask import Flask, jsonify
import os  # 新添加的模块，用于支持 Render 的动态端口

app = Flask(__name__)

# 固定返回的目标攻击地址
ATTACK_ADDRESS = "panteklu-target"

@app.route('/get_target_address', methods=['GET'])
def get_target_address():
    """
    返回固定的攻击地址。
    """
    return jsonify({"attack_address": ATTACK_ADDRESS}), 200

@app.route('/', methods=['GET'])  # 新增代码
def home():
    """
    默认的根路径响应，避免 / 访问返回 404。
    """
    return jsonify({"message": "Welcome to the Cloud Service!"}), 200

if __name__ == "__main__":
    # 动态绑定 Render 提供的端口，默认5000
    PORT = int(os.environ.get('PORT', 5000))  # 新增代码
    app.run(host="0.0.0.0", port=PORT)
