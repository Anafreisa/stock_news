import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = ALPHA VANTAGE API KEY
NEWS_API_KEY = NEWS API KEY
account_sid = YOUR ACCOUNT SID
auth_token = YOUR TOKEN

alpha_vantage_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=alpha_vantage_parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
day_before_data = data_list[1]
day_before_closing_price = float(day_before_data["4. close"])

price_variation = round((yesterday_closing_price - day_before_closing_price)/yesterday_closing_price * 100, 4)

signal = None
if price_variation > 0:
    signal = "🔺"
elif price_variation < 0:
    signal = "🔻"

if abs(price_variation) > 5:
    response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    response.raise_for_status()
    news_data = response.json()
    news_slice = news_data["articles"][:3]

    for articles in news_slice:
        articles_list = [articles["title"], articles["description"]]

        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"{STOCK_NAME}: {signal}{price_variation}%\n\nHeadline: {articles_list[0]}\n\n"
                 f"Brief: {articles_list[1]}",
            from_= TWILIO NUMBER,
            to= TWILIO VERIFIED NUMBER
        )
        print(message.status)
