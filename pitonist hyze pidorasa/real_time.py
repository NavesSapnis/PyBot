import datetime
import threading

dt = datetime.datetime.now()
dt_string = dt.strftime("Date: %d/%m/%Y  time: %H:%M:%S")
#print(dt_string)

def start():
    with open("config/top.txt", "w") as file:
        file.write(f"\tТоп 10 криптовалют по капитализации и их цена {dt_string}\n")

t = threading.Thread(target=start)