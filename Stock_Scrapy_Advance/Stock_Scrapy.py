import os.path
import requests
import csv
import time
from bs4 import BeautifulSoup


class StockScrapy():
    def __init__(self, url):
        self.__URL = url
        self.__headers = ''
        self.__result = []

    def scrapy_stock_information(self):
        res = requests.get(self.__URL)
        if not res.ok:
            print("Request fail!")
            exit()
        soup = BeautifulSoup(res.text, "html.parser")
        self.__headers = soup.select_one(".table-header-wrapper").find_all(string=True)
        self.__headers = self.__headers.pop(0).split("/") + self.__headers
        print(self.__headers)
        self.__headers.append("漲跌符號")
        self.__result = []
        for element in soup.select("#hero-0-MarketTable-Proxy li"):
            row = element.find_all(string=True)
            # 漲跌符號
            if element.find_all(class_="C($c-trend-up)"):
                row.append("^")
            elif element.find_all(class_="C($c-trend-down)"):
                row.append("v")
            else:
                row.append("-")
            self.__result.append(dict(zip(self.__headers, row)))
        #print(self.result)
        return self.__headers, self.__result

    def save_as_csv_report(self, folder_path,Title,Datas):
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        fn = folder_path+'\\'+time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime()) + '_Yahoo_StockInformation.csv'
        with open(fn, 'w') as csvfile:
            writer = csv.writer(csvfile)
            #先寫標題
            writer.writerow(Title)
            #寫內容
            for data in Datas:
                writer.writerow(data.values())
