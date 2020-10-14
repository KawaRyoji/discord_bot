import requests
import datetime
from bs4 import BeautifulSoup

class scraping:
    def forecast(self, *city_name: str):
        res = self.__fetch_forecast_data_from_yahoo(city_name)
        
        return res

    def __fetch_forecast_data_from_yahoo(self, *city_names: str):
        weekday = ["月", "火", "水", "木", "金", "土", "日"]

        forecast_site = {
            "名古屋": "https://weather.yahoo.co.jp/weather/jp/23/5110.html",
            "横浜": "https://weather.yahoo.co.jp/weather/jp/14/4610.html"
        }
        today_date = datetime.date.today()
        tomorrow_date = today_date + datetime.timedelta(days=1)

        res_today    = "今日 {}月{}日({})の天気\n".format(today_date.month, today_date.day, weekday[today_date.weekday()])
        res_tomorrow = "明日 {}月{}日({})の天気\n".format(tomorrow_date.month, tomorrow_date.day, weekday[tomorrow_date.weekday()])
        
        for city_name in city_names[0]:
            if not city_name in forecast_site:
                raise Exception("指定した街の名前のwebサイトが登録されていません")

            res = requests.get(forecast_site[city_name])
            soup = BeautifulSoup(res.text, "html.parser")

            today_forecast  = soup.select_one("#main > div.forecastCity > table > tr > td > div")
            today_whether   = today_forecast.select_one("p.pict").text
            today_temp_high = today_forecast.select_one("ul.temp > li.high > em").text
            today_temp_low  = today_forecast.select_one("ul.temp > li.low > em").text

            tomorrow_forecast   = soup.select_one("#main > div.forecastCity > table > tr > td + td > div")
            tomorrow_whether    = tomorrow_forecast.select_one("p.pict").text
            tomorrow_temp_high  = tomorrow_forecast.select_one("ul.temp > li.high > em").text
            tomorrow_temp_low   = tomorrow_forecast.select_one("ul.temp > li.low > em").text

            res_today    += "{}:\n\t天気: {}\n\t最高気温: {}℃\n\t最低気温: {}℃\n".format(city_name, today_whether, today_temp_high, today_temp_low)
            res_tomorrow += "{}:\n\t天気: {}\n\t最高気温: {}℃\n\t最低気温: {}℃\n".format(city_name, tomorrow_whether, tomorrow_temp_high, tomorrow_temp_low)
        
        return res_today + "\n" + res_tomorrow
