import json
import os
import platform
import requests
from shutil import copyfileobj
from importlib import resources  # Python 3.9+ 可用


def download_and_install_font(font_name, font_url, install_dir):
    """
    Download and install a font from the given URL.
    """
    try:
        print(f"Downloading {font_name}...")
        response = requests.get(font_url, stream=True)
        response.raise_for_status()

        # 保存字体文件到本地
        font_path = os.path.join(
            install_dir, f"{font_name}.ttf"
        )  # 或者使用 .otf 根据实际情况
        with open(font_path, "wb") as f:
            copyfileobj(response.raw, f)

        print(f"{font_name} installed successfully at {install_dir}!")
    except Exception as e:
        print(f"Failed to install {font_name}: {e}")


def install_fonts():
    """
    Install predefined fonts.
    """
    try:
        with resources.open_text("texfont", "font_list.json") as f:
            fonts = json.load(f)
    except Exception as e:
        print(f"Failed to load font list: {e}")
        return

    # 根据操作系统确定字体安装目录
    system = platform.system()
    if system == "Linux":
        install_dir = os.path.expanduser("~/.fonts")
    elif system == "Darwin":  # macOS
        install_dir = os.path.expanduser("~/Library/Fonts")
    elif system == "Windows":
        install_dir = os.path.join(os.getenv("C://Windows"), "Fonts")
    else:
        raise OSError("Unsupported operating system")

    # 创建字体目录（如果不存在的话）
    os.makedirs(install_dir, exist_ok=True)

    # 下载并安装每个字体
    for font_name, font_url in fonts.items():
        download_and_install_font(font_name, font_url, install_dir)
