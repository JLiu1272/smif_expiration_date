import requests
from datetime import timedelta
import datetime

url = "http://107.23.213.161/expiration_database.json"

"""
Type = Where is the food being placed
0 - Room Temperature
1 - Refrigerator
2 - Freezer at 0 F
"""
def getRequest(url, food, type):
    r = requests.get(url)
    json = r.json()
    return json[food][type]

def computeDateLeft(date, food, type):
    today = datetime.datetime.now()
    data = getRequest(url, food, type)
    dateleft = ""

    if type == 2 and data == "" or data == "\u00a0":
        return "Unable to get value"
    elif data == "" or data == "\u00a0":
        return computeDateLeft(today, food, type+1)
    elif "month" in data or "months" in data:
        week = int(data[0])*365/12
        print("Month: " + str(week))
        dateleft = date + timedelta(week)
    elif "day" in data or "days" in data:
        dateleft = date + timedelta(days=data[0])
    elif "year" in data or "years" in data:
        year = int(data[0])*365
        dateleft = date + timedelta(int(year))

    return dateleft


def main():
    today = datetime.datetime.now()
    data = getRequest(url, "Canned fruit", 0)
    print(data)
    print("Today:  " + str(today))
    print("Data: " + str(data))
    print(computeDateLeft(today, "Canned fruit", 0))

if __name__ == "__main__":
    main()