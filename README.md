<h1 style="text-align: center">PixelSpider | PyDemo</h1>

<div style="text-align: center"><img style="width: 48px;border-radius: 6px;" src="./assets/logo.png"/></div>

# 使用说明

## 爬取 Wallhaven.cc

<sup>示例见：example-wallhaven.py</sup>

1. 安装相关 Python 依赖

```bash
pip install requests
```

2. 使用浏览器登录[wallhaven.cc](https://wallhaven.cc/)，替换下方代码中的 `Cookie`，并选择合适位置进行下载

```bash
wallhaven.save_wallhaven(url=url,startPage=27,endPage=100,directPath="/Users/xxx/Desktop",cookies=cookies)
```
## 爬取彼岸图库

<sup>示例见：example-bianpic.py</sup>

1. 安装相关 Python 依赖

```bash
pip install requests
```

2. 使用浏览器登录[pic.netbian.com/](https://pic.netbian.com/)，替换下方代码中的 `Cookie`，并选择合适位置进行下载


3. 可以适当的修改下间隔时长（彼岸图库爬取太快的话会导致Cookie失效，需要重新登录才可以）