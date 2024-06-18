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
    url = f"https://tw.stock.yahoo.com/quote/{stock_num[i]}"  # Yahoo's url
    web = requests.get(url)  # get html content
    soup = BeautifulSoup(web.text, "html.parser")
    title = soup.find("h1")  # Find h1 content
    a = soup.select(".Fz\(32px\)")[
        0
    ]  # Find first class content have Fz(32px) ，if error，use.Fz\(32px\)
    b = soup.select(".Fz\(20px\)")[
        1
    ]  # Find first class content have Fz(20px) if error，use.Fz\(20px\)
    s = ""  # up/down trend
    try:
        # if main-0-QuoteHeader-Proxy id 'S div have C($c-trend-down) is means down trend，elif C($c-trend-up) means up trend
        if soup.select("#main-0-QuoteHeader-Proxy")[0].select(".C\\(\\$c-trend-up\\)"):
            s = "+"
        elif soup.select("#main-0-QuoteHeader-Proxy")[0].select(
            ".C\\(\\$c-trend-down\\)"
        ):
            s = "-"
        print(
            f"{title.get_text()} {stock_num[i]}: {a.get_text()} ( {s}{b.get_text()} )"
        )
    except:
        s = "Error"
        print(s)  # Error Msg
