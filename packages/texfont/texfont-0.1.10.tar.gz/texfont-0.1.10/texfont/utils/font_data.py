from http.client import responses
from urllib.parse import unquote

import requests
import json

from tqdm import tqdm

API_URL = "https://api.github.com/repos/google/fonts/contents/ofl"

ACCESS_TOKEN = "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"
HEADERS = {"Authorization": f"token {ACCESS_TOKEN}"}


def fetch_ofl_list_json(api_url=API_URL, is_admin=False):
    """
    :param api_url:
    :param is_admin:
    :return:
    {
        "name": "abeezee",
        "path": "ofl/abeezee",
        "sha": "83498679c7af31b3e2f28d05e812f6f81c9fe4f6",
        "size": 0,
        "url": "https://api.github.com/repos/google/fonts/contents/ofl/abeezee?ref=main", # WE NEED THIS!
        "html_url": "https://github.com/google/fonts/tree/main/ofl/abeezee",
        "git_url": "https://api.github.com/repos/google/fonts/git/trees/83498679c7af31b3e2f28d05e812f6f81c9fe4f6",
        "download_url": null,
        "type": "dir",
        ...
    }
    """
    if is_admin:
        response = requests.get(api_url, headers=HEADERS)
    else:
        response = requests.get(api_url)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        return json_data
    else:
        print("Failed to fetch github")
        return None


def get_ttf_download_url_list_json(url_content):
    """

    :param url_content:
    [
        {
            "path": "ABeeZee-Italic.ttf",
            "mode": "100644",
            "type": "blob",
            "sha": "da4bf4754d583f833e0dd276094697275c0a53d2",
            "size": 47012,
            "url": "https://api.github.com/repos/google/fonts/git/blobs/da4bf4754d583f833e0dd276094697275c0a53d2"
        },
        {
            "path": "ABeeZee-Regular.ttf",
            "mode": "100644",
            "type": "blob",
            "sha": "2ecf01bdec7b6a8568825da840897f9b0aee8a86",
            "size": 46016,
            "url": "https://api.github.com/repos/google/fonts/git/blobs/2ecf01bdec7b6a8568825da840897f9b0aee8a86"
        }
        ...
    ]

    :return:
    """
    download_url_list = []
    if url_content:
        for item in url_content:
            if ".ttf" in str(item["path"]):
                download_url_list.append(item["download_url"])
        return download_url_list
    else:
        return None


def get_font_names(ofl_font_json_list):
    font_names = []
    for font_json in ofl_font_json_list:
        font_names.append(font_json["name"])
    return font_names


def fetch_ttf_url_download_list_by_name(font_name, is_admin=False, force=False):
    tqdm.write("Fetching fonts formulas from https://api.github.com/repos/google/fonts/contents/ofl")
    ofl_list = fetch_ofl_list_json(API_URL, is_admin=is_admin)
    tqdm.write("Successfully fetched fonts formulas")

    all_font_names = get_font_names(ofl_list)
    if font_name not in all_font_names and not force:
        print(f"{font_name} not found in ofl_list")
        print("Using following font names:")
        for font_name in all_font_names:
            print(font_name)
        return None
    for ofl in ofl_list:
        if force:
            url = f"https://api.github.com/repos/google/fonts/contents/ofl/{font_name}?ref=main"
        else:
            url = ofl["url"]
        tqdm.write(f"Fetching fonts {font_name} from formulas")
        url_content = json.loads(
            requests.get(url,
                         headers=HEADERS if is_admin else None).text)
        tqdm.write(f"Successfully fetched fonts {font_name} from formulas")
        download_list = []
        for download in get_ttf_download_url_list_json(url_content):
            name = unquote(download.split("/")[-1])
            download_url = download
            download_list.append({
                "name": name,
                "download_url": download_url,
            })

        if download_list:
            return download_list
        return None


if __name__ == '__main__':
    ttf_download_list = fetch_ttf_url_download_list_by_name("abeezee", True)
    print(ttf_download_list)
