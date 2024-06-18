import requests
from bs4 import BeautifulSoup

stock_num = []
x = 1
while x == 1:
    num = input("輸入要查詢的股票代號:")
    if num != "ok":
        stock_num.append(num)
    else:
        x = -1
for i in range(len(stock_num)):
    url = f"https://tw.stock.yahoo.com/quote/{stock_num[i]}"  # 台積電 Yahoo 股市網址
    web = requests.get(url)  # 取得網頁內容
    soup = BeautifulSoup(web.text, "html.parser")  # 轉換內容
    title = soup.find("h1")  # 找到 h1 的內容
    a = soup.select(".Fz\(32px\)")[0]  # 找到第一個 class 為 Fz(32px) 的內容，如果出現錯誤，可以使用 .Fz\(32px\) 轉義
    b = soup.select(".Fz\(20px\)")[0]  # 找到第一個 class 為 Fz(20px) 的內容，如果出現錯誤，可以使用 .Fz\(20px\) 轉義
    s = ""  # 漲或跌的狀態
    try:
    # 如果 main-0-QuoteHeader-Proxy id 的 div 裡有 C($c-trend-down) 的 class
    # 表示狀態為下跌
        if soup.select("#main-0-QuoteHeader-Proxy")[0].select(".C($c-trend-down)")[0]:
            s = "-"
    except:
        try:
        # 如果 main-0-QuoteHeader-Proxy id 的 div 裡有 C($c-trend-up) 的 class
        # 表示狀態為上漲
            if soup.select("#main-0-QuoteHeader-Proxy")[0].select(".C($c-trend-up)")[0]:
                s = "+"
        except:
        # 如果都沒有包含，表示平盤
            s = "-"
    print(f"{title.get_text()} {stock_num[i]}: {a.get_text()} ( {s}{b.get_text()} )")  # 印出結果
