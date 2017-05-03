import requests
from datetime import timedelta
import datetime
import re
import json

url_exp = "http://107.23.213.161/expiration_database.json"
url_add = "http://107.23.213.161/addItem.php"

"""
Type = Where is the food being placed
0 - Room Temperature
1 - Refrigerator
2 - Freezer at 0 F
"""
def getRequest(url, food, type):
    r = requests.get(url)
    json = r.json()
    lower_food = food.lower()

    filtered = {}
    print(json[lower_food])
    if lower_food not in json.keys():
        for key in json:
            regex = r"" + re.escape(lower_food)
            need_match = re.search(regex, key)
            if need_match is not None:
                filtered[need_match.group(0)] = json[key]
                return filtered[need_match.group(0)][type]
    return json[lower_food][type]

"""
Post data to database
"""
def post_data(url,food, date_in, date_left):
    data = {'name': "002" + food, 'date_in': date_in, 'date_left': date_left}
    r = requests.post(url, data)
    print(r.text)

"""
Compute Expiration Date
"""
def computeDateLeft(date, food, type):
    today = datetime.datetime.now()
    data = getRequest(url_exp, food, type)
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
        dateleft = date + timedelta(days=int(data[0]))
    elif "year" in data or "years" in data:
        year = int(data[0])*365
        dateleft = date + timedelta(int(year))
    elif "week" in data or "weeks" in data:
        week = int(data[0])
        dateleft = date + timedelta(week)

    return dateleft


def main():
    today = datetime.datetime.now()
    food = "Cereals"
    date_left = computeDateLeft(today, food, 1)

    data = getRequest(url_exp, food, 1)
    #print(data)
    print("Today:  " + str(today))
    print("Data: " + str(data))
    print(date_left)
    post_data(url_add, food, today, date_left)

if __name__ == "__main__":
    main()