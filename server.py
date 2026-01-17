from flask import Flask, jsonify

app = Flask(__name__)

# 固定返回的目标攻击地址
ATTACK_ADDRESS = "panteklu-target"

@app.route('/get_target_address', methods=['GET'])
def get_target_address():
    """
    返回固定的攻击地址。
    """
    return jsonify({"attack_address": ATTACK_ADDRESS}), 200

if __name__ == "__main__":
    # 运行服务，监听所有地址，端口5000
    app.run(host="0.0.0.0", port=5000)