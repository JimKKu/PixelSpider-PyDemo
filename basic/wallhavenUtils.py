import re
from time import process_time_ns

import requests

from fileUtils import fileUtils

"""
项目说明
1. 调用wallhaven.save_wallhaven()方法，可以爬取wallhaven页面的所有壁纸
2. URL为必填项，将想要抓取的页面的URL输入进去，点击开始即可摘取
3. 默认仅抓取第一页的内容，可以用startPage/endPage来控制抓取的页面范围（通常一个页面为24张图片所有）
4. directPath为存储位置，默认为项目的运行位置，改变后可以存储在其他位置
5. cookies为浏览器中的Cookie，若摘取普通壁纸，则可以不填写，若抓取NSFW壁纸，则需要复制浏览器地址填写
6. headers为浏览器中的User_Agent/Accept，一般不需要填写
"""


# ---------------------------------------------------------------------------------------------------------------------------


"""
判断URL中是否含有page=xx，有的话删除掉，返回不带Page信息的URL
"""
def get_url_without_page_info(url: str) -> str:

    if url is None:
        raise ValueError('url is None')
    regex = re.compile(r"page=\d+", re.S)
    page_info = regex.search(url)

    if page_info:
        # 删除pageInfo信息
        url = url.replace(page_info[0],'')

        if url.__contains__("&&"):
            return url.replace("&&", "&")
        if url.__contains__("?&"):
            return url.replace("?&", "?")
        if url.endswith("&") or url.endswith("?"):
            return url[:-1]
    return url

"""
刷新Cookie
"""
def refresh_token(url:str,cookies:str=None,headers:dict=None) -> str:
    session = requests.Session()
    resp = session.get(url,headers=headers,cookies=cookies)
    return resp.cookies.get_dict().get('XSRF-TOKEN')


"""
获取图片后缀
"""
def get_img_suffix(url:str) -> str:
    if url is None:
        raise ValueError('url is None')
    regex = re.compile(r'https://.*\.(?P<suffix>.*?) ', re.S)
    url = url+' '
    suffix = regex.search(url).group("suffix")
    return suffix.replace(' ','')




"""
获取完整URL | 带有PageInfo
"""
def get_index_url(url:str,pageNum:int) -> str:
    if url is None:
        raise ValueError('url is None')
    if get_url_without_page_info(url) is not None:
        if url.__contains__("?") or url.__contains__("&"):
            return f'{url}&page={pageNum}'
        else:
            return f'{url}?page={pageNum}'
    return url



class wallhaven:
    headers = {
        "User_Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }
    Cookie = ""

    @classmethod
    def save_wallhaven(cls,url:str,startPage:int = 1,endPage:int=2,directPath:str='./',cookies:dict=None,headers:dict=None):

        if url == r'https://wallhaven.cc/':
            raise ValueError('不能爬取首页哦~~')
        if directPath.endswith(r'/'):
            directPath = directPath[:-1]
        if headers == {}:
            headers = cls.headers
        # 获取一个新的Cookie并抓取
        if cookies == {}:
            cookie_str = refresh_token(url,headers=headers,cookies=cls.Cookie)
            cookies = {"Cookie":cookie_str}
            print(f"Cookie新1 -- :{cookies}")

        """
        一些规则，分别用于：
        1. 从主页中获取子页面URL
        2. 从子页面中获取图片URL
        3. 从图片URL中获取后缀
        """
        regex1 = re.compile(r'img alt="loading" class="lazyload".*?href="(?P<url_son_page>.*?)"', re.S)
        regex2 = re.compile(r'img id="wallpaper" src="(?P<url_img>.*?)"', re.S)

        for i in range(startPage, endPage):
            # 获取完整的首页Index
            url_father = get_index_url(url,i)
            print(f"循环第{i}次")
            # 获取新的Cookie
            session = requests.Session()
            print(f"当前Cookies:{cookies}")
            resp = session.get(url_father, headers=headers,cookies=cookies)
            cookie_new= resp.cookies# 获取一个新的Cookie
            if cookie_new is not None and cookie_new != cookies:
                cookies = cookie_new
                print(f"-- Page {i} -- 更换cookie：「{cookies}」")
            # 获取父页面信息
            resp1 = requests.get(url=url_father, headers=headers, cookies=cookies)
            # 不保存父页面
            # fileUtils.save(f"./8.测试封装wallhaven/ss/index-page-{i}.html", resp1.text)
            item_son_urls = regex1.finditer(resp1.text)
            x = 0
            for item in item_son_urls:
                x += 1
                url_son_page = item.group("url_son_page")
                resp2 = requests.get(url_son_page, headers=headers, cookies=cookies)

                # url_img 的地址，再从里面获取fileName
                url_img = regex2.findall(resp2.text)
                if url_img == []:
                    fileUtils.appendBr(f"{directPath}/logs.txt", f"-- [图{x}] 获取失败，网页地址为:{url_son_page}")
                    print(f"-- [{x}] -- [{url_son_page}] --")
                    continue
                url_img = url_img[0]
                # URL为空 | 记录子页面链接
                if(url_img == ''):
                    fileUtils.appendBr(f"{directPath}/logs",url_son_page)

                # 获取图片+图片后缀 | 并保存图片
                resp3 = requests.get(url_img, headers=headers, cookies=cookies)
                last_name = get_img_suffix(url_img)
                print(f"-- [{i}-{x}] -- {url_img} -- {len(resp3.content)} -- {last_name}")
                fileUtils.saveBytes(f"{directPath}/img-{i}-{x}.{last_name}", resp3.content)
                resp2.close()

            resp1.close()

