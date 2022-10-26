import requests
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import creds

stock_name = "TSLA"
COMPANY_NAME = "Tesla Inc"

stock_endpoint = "https://www.alphavantage.co/query"
news_endpoint = "https://newsapi.org/v2/everything"



def get_response(symbol, today, yesterday):
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": creds.alpha_apikey
    }
    response = requests.get(stock_endpoint, params=stock_params)
    data = response.json()

    today_open = float(data["Time Series (Daily)"][today]["1. open"])
    yesterday_close = float(data["Time Series (Daily)"][yesterday]["4. close"])

    difference = today_open - yesterday_close
    percent = round(((difference/yesterday_close) * 100), 2)
    return percent

def getNews(name: str):
    """
    Using the name of a stock as an argument, it returns a list of three articles, their description and urls.
    """
    news_params = {
        "q": name,
        "apiKey": creds.news_apikey
    }
    response1 = requests.get(news_endpoint, params=news_params)
    data = response1.json()
    articles, descriptions, urls = [], [], []
    for i in range(3):
        articles.append(data["articles"][i]["title"])
        descriptions.append(data["articles"][i]["description"])
        urls.append(data["articles"][i]["url"])

    return articles, descriptions, urls

def main():
    symbol = stock_entry.get()
    name = name_entry.get()

    today_date = str(datetime.now().date()).split("-")
    today = "-".join([today_date[0], today_date[1], str(int(today_date[2]))])
    yesterday = "-".join([today_date[0], today_date[1], str(int(today_date[2])-1)])
    try:
        percent = get_response(symbol, today, yesterday)
        if percent > 0:
            message = f"{symbol}🔺: {percent}%"
        else:
            message = f"{symbol}🔻: {percent}%"
        articles, descriptions, urls = getNews(name)
        article_message1 = f" {articles[0]} \n\n {descriptions[0]} \n {urls[0]}"
        article_message2 = f" {articles[1]} \n\n {descriptions[1]} \n {urls[1]}"
        article_message3 = f" {articles[2]} \n\n {descriptions[2]} \n {urls[2]}"

    except KeyError:
        messagebox.showinfo(title="Error", message="No data for current date found.")
    else:
        messagebox.showinfo(title="Stock info", message=message)
        messagebox.showinfo(title="Stock info", message=article_message1)
        messagebox.showinfo(title="Stock info", message=article_message2)
        messagebox.showinfo(title="Stock info", message=article_message3)

# Tkinter Window Setup

window = Tk()
window.title("Check your stocks")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="market.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

#Labels
stock_label = Label(text="Stock symbol:")
stock_label.grid(row=1, column=0)

stock_name = Label(text="Stock name:")
stock_name.grid(row=2, column=0)

#Entries
stock_entry = Entry(width=20)
stock_entry.grid(row=1,column=1)
stock_entry.focus()
name_entry = Entry(width=20)
name_entry.grid(row=2,column=1)
name_entry.focus()

#Buttons
search_button = Button(text="Search", width=14, command=main)
search_button.grid(row=3, column=1)


window.mainloop()


