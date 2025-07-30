<h1 style="text-align: center">PixelSpider | PyDemo</h1>

<div style="text-align: center"><img style="width: 48px;border-radius: 6px;" src="./assets/logo.png"/></div>

# 使用方式

## 爬取 Wallhaven.cc

<sup>示例见：wallhaven-example.py</sup>

1. 安装相关 Python 依赖

```bash
pip install requests
```

2. 使用浏览器登录[wallhaven.cc](https://wallhaven.cc/)，替换下方代码中的 `Cookie`，并选择合适位置进行下载

```bash
wallhaven.save_wallhaven(url=url,startPage=27,endPage=100,directPath="/Users/xxx/Desktop",cookies=cookies)
```