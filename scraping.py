import requests
from bs4 import BeautifulSoup

class scraping:
    whether_nagoya_site = "https://weather.yahoo.co.jp/weather/jp/23/5110.html"
    whether_yokohama_site = "https://weather.yahoo.co.jp/weather/jp/14/4610.html"

    def forecast(self):
        res_n = requests.get(self.whether_nagoya_site)
        res_y = requests.get(self.whether_yokohama_site)
        soup_n = BeautifulSoup(res_n.text, "html.parser")
        soup_y = BeautifulSoup(res_y.text, "html.parser")

        today_forecast_nagoya = soup_n.select_one('#main > div.forecastCity > table > tr > td > div')
        today_forecast_yokohama = soup_y.select_one('#main > div.forecastCity > table > tr > td > div')
        tomorrow_forecast_nagoya = soup_n.select_one('#main > div.forecastCity > table > tr > td + td > div')
        tomorrow_forecast_yokohama = soup_y.select_one('#main > div.forecastCity > table > tr > td + td > div')

        today = today_forecast_nagoya.select_one("p").text
        today_whether_nagoya = today_forecast_nagoya.select_one("p.pict").text
        today_temp_high_nagoya = today_forecast_nagoya.select_one("ul.temp > li.high > em").text
        today_temp_low_nagoya = today_forecast_nagoya.select_one("ul.temp > li.low > em").text
        
        today_whether_yokohama = today_forecast_yokohama.select_one("p.pict").text
        today_temp_high_yokohama = today_forecast_yokohama.select_one("ul.temp > li.high > em").text
        today_temp_low_yokohama = today_forecast_yokohama.select_one("ul.temp > li.low > em").text

        tomorrow = tomorrow_forecast_nagoya.select_one("p").text
        tomorrow_whether_nagoya = tomorrow_forecast_nagoya.select_one("p.pict").text
        tomorrow_temp_high_nagoya = tomorrow_forecast_nagoya.select_one("ul.temp > li.high > em").text
        tomorrow_temp_low_nagoya = tomorrow_forecast_nagoya.select_one("ul.temp > li.low > em").text
        
        tomorrow_whether_yokohama = tomorrow_forecast_yokohama.select_one("p.pict").text
        tomorrow_temp_high_yokohama = tomorrow_forecast_yokohama.select_one("ul.temp > li.high > em").text
        tomorrow_temp_low_yokohama = tomorrow_forecast_yokohama.select_one("ul.temp > li.low > em").text
        
        res = "今日 {}の天気\n".format(today)
        res += "名古屋:\n\t天気: {}\n\t最高気温: {}℃\n\t最低気温: {}℃\n".format(today_whether_nagoya, today_temp_high_nagoya, today_temp_low_nagoya)
        res += "横浜　:\n\t天気: {}\n\t最高気温: {}℃\n\t最低気温: {}℃\n".format(today_whether_yokohama, today_temp_high_yokohama, today_temp_low_yokohama)
        
        res += "\n明日 {}の天気\n".format(tomorrow)
        res += "名古屋:\n\t天気: {}\n\t最高気温: {}℃\n\t最低気温: {}℃\n".format(tomorrow_whether_nagoya, tomorrow_temp_high_nagoya, tomorrow_temp_low_nagoya)
        res += "横浜　:\n\t天気: {}\n\t最高気温: {}℃\n\t最低気温: {}℃\n".format(tomorrow_whether_yokohama, tomorrow_temp_high_yokohama, tomorrow_temp_low_yokohama)
        
        return res
