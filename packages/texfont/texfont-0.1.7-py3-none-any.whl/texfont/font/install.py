import os
import platform
import requests
from shutil import copyfileobj
import tqdm

from texfont.utils.font_data import fetch_ttf_url_download_list_by_name, fetch_ofl_list_json, get_font_names


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
            install_dir, f"{font_name}"
        )  # 或者使用 .otf 根据实际情况
        with open(font_path, "wb") as f:
            copyfileobj(response.raw, f)

        print(f"{font_name} installed successfully at {install_dir}!")
    except Exception as e:
        print(f"Failed to install {font_name}: {e}")


def install_fonts(names: list[str], is_admin=False):
    """
    Install predefined fonts.
    """
    # 根据操作系统确定字体安装目录
    system = platform.system()
    if system == "Linux":
        install_dir = os.path.expanduser("~/.fonts")
    elif system == "Darwin":  # macOS
        install_dir = os.path.expanduser("~/Library/Fonts")
    elif system == "Windows":
        install_dir = os.path.expanduser("C:\\Windows\\Fonts")
    else:
        raise OSError("Unsupported operating system")

    all_list_to_download = []
    # 创建字体目录（如果不存在的话）
    os.makedirs(install_dir, exist_ok=True)
    for name in names:
        for item in fetch_ttf_url_download_list_by_name(name, is_admin=is_admin):
            all_list_to_download.append(item)
    for item in tqdm.tqdm(all_list_to_download):
        download_and_install_font(item["name"], item["download_url"], install_dir)


def install_all_fonts(is_admin: False):
    ofl_list = fetch_ofl_list_json(is_admin=is_admin)
    all_fonts = get_font_names(ofl_list)
    install_fonts(all_fonts, is_admin=is_admin)
