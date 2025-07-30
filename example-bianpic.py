import requests
import time
import re
from urllib.request import urlopen

from bisic.fileUtils import fileUtils

base_url = "https://pic.netbian.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

cookies = {
    "Cookie": "PASTE YOUR COOKIE HERE"
}


obj = re.compile(r'token=(?P<token>.*?)"}',re.S)
for i in range(36908,1,-1):
    url = f"{base_url}/e/extend/downpic.php?id={str(i)}&t=0.42531204335457073"
    resp = requests.get(url,headers=headers,cookies=cookies)
    resp.encoding = "utf-8"
    print(resp.text)
    token = obj.findall(resp.text)[0]



    url_img = f"{base_url}/e/extend/downpic.php?id={str(i)}&token={token}"
    print(f"{url_img} -- {len(token)} -- {token}")

    resp_img = requests.get(url_img, headers=headers, cookies=cookies)
    if len(resp_img.content) > 8:
        fileUtils.saveBytes(f"./7.彼岸图库_imgs/bian-{str(i)}.jpg", resp_img.content)
    else:
        fileUtils.appendBr(f"./7.彼岸图库_imgs/log.txt",f"{i} -- {token} -- {resp.text}")

    time.sleep(6)