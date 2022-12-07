from time import sleep
import urllib.parse
import urllib.request
import webbrowser
import requests
from bs4 import BeautifulSoup
import threading
import real_time


real_time.t.start()

def get_cur():
    cc=0
    coin=0
    while cc<=10:
        url= "http://www.coingecko.com/ru"
        try:
            r = requests.get(url)
            soup=BeautifulSoup(r.text,features="html.parser")
            coin_kurs = list(soup.find_all('td', {'class': 'td-price price text-right pl-0'})[cc].get_text())
            coin_name = list(soup.find_all('span', {'class': 'tw-hidden d-lg-inline font-normal text-3xs ml-2'})[coin].get_text())


            coin_kurs.pop(0)
            coin_name.pop(0)

            full_name=""
            for index in range(len(coin_name)):
                full_name+=coin_name[index]

            coin_price= ""
            for i in range(len(coin_kurs)):
                coin_price+=coin_kurs[i]
            
            all=full_name+" "+coin_price+"\n"
            print (f"{cc*10}/100%")
            with open("config/top.txt", "a") as file:
                file.write(all)

            cc+=1
            coin+=1
            if cc==10:
                print("Отгрузил проверяй\nОтключение...")
            else:
                pass
        except:
            pass