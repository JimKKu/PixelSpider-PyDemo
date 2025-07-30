from basic.wallhavenUtils import wallhaven

url="https://wallhaven.cc/search?q=id%3A108736&categories=111&purity=111&sorting=date_added&order=desc&ai_art_filter=0"
cookies={"Cookie":"PASTE YOUR COOKIE HERE"}


wallhaven.save_wallhaven(url=url,startPage=27,endPage=100,directPath="/Users/hsk/Desktop/ChunMomo",cookies=cookies)
