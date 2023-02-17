#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import json
import requests
from Crypto.Cipher import AES

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        # "Content-Type": "application/json",
        # "Referer": f"https://ke.qq.com/webcourse/index.html?cid={course_id}&term_id=100421954&taid=1468759704059259",
        'referer': 'https://ke.qq.com/course/457935/4057017518324943',
        'cookie': 'pac_uid=0_c27b242f6442f; iip=0; pgv_pvid=9509777675; tdw_data_testid=; tdw_data_flowid=; uid_uin=144115197334994475; uid_type=2; openid=oTpUI0T7eD8qf7ssoBXJgrFTCfI8; uid_appid=1400000008; uid_a2=30ff7919578416d0a2562e581c210447b483011c0db2af576ed5a3b6cd32fb646509afc5a28073937f137e35b12683a8bf3302a369f2bf0e021f712e602736d7fad7edde310e8971; sessionPath=16766142403241596996316; auth_version=2.0; uin=144115197334994475; p_uin=144115197334994475; p_luin=144115197334994475; uid_origin_uid_type=2; uid_origin_auth_type=2; pgv_info=ssid=s6667806676; _pathcode=0.32583535129713637; tdw_auin_data=-; tdw_data={"ver4":"4","ver6":"","refer":"","from_channel":"","path":"r-0.32583535129713637","auin":"-","uin":144115197334994475,"real_uin":"144115197334994475"}; ke_login_type=2; tdw_first_visited=1; iswebp=1; tdw_data_new_2={"auin":"-","sourcetype":"","sourcefrom":"","ver9":"144115197334994475","uin":"144115197334994475","visitor_id":"12224671161625245","ver10":"","url_page":"","url_module":"","url_position":"","sessionPath":"16766142403241596996316"}',
    }

    params = {
        'course_id': 457935,
        'file_id': 5285890807361215387,
        'header': '{"uin":"144115197334994475","srv_appid":201}',
        'term_id': 100547988,
    }

    response = requests.get("https://ke.qq.com/cgi-proxy/rec_video/describe_rec_video?", headers=headers, params=params)
    print(response)
    if response.status_code == 200:
        content = json.loads(response.content)
        print(content)


def decrypt_ts(key,iv,data):
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.decrypt(data)

def download_ts(url, key, iv):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content
        return decrypt_ts(key, iv, data)
    else:
        print("Download failed.")
        return None

def parse_m3u8(m3u8_url, key, iv):
    response = requests.get(m3u8_url)
    if response.status_code == 200:
        m3u8_content = response.text
        lines = m3u8_content.split("\n")
        ts_urls = [line for line in lines if line.endswith(".ts")]
        for ts_url in ts_urls:
            data = download_ts(ts_url, key, iv)
            with open(ts_url.split("/")[-1], "wb") as f:
                f.write(data)
        print("All ts files downloaded.")
    else:
        print("Failed to get m3u8 content.")



if __name__ == '__main__':
    main()
    