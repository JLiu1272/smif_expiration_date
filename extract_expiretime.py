#import statements for all necessary components
from bs4 import BeautifulSoup
import urllib.request
import pprint

#Exporting extracted data as CSV
import csv
import json

#specify the url
source = "http://food.unl.edu/food-storage-chart-cupboardpantry-refrigerator-and-freezer"

#CSV File
csvfile = "test.csv"

#Query the website and return the html to the variable 'page'
page = urllib.request.urlopen(source)

#Parse the html in the 'page' variable, and store it in Beautiful Soup format
soup = BeautifulSoup(page, "html.parser")

"""
Grabbing data from website
"""
def extract_details():
    header = []
    title = soup.find_all('span', {'class': 'style4'})
    for i in title:
        header.append(i.text)
    dict = {}
    table = soup.find_all('table')

    for tag in table:
        for tr in tag.find_all('tr'):
            tab_det = tr.find_all('td')
            if len(tab_det) == 4:
                if tab_det[1].text == '\xa0':
                    dict.update({tab_det[0].text.lower(): ['', tab_det[2].text.lower(), tab_det[3].text.lower()]})
                elif tab_det[2].text == '\xa0':
                    dict.update({tab_det[0].text.lower(): [tab_det[1].text.lower(), '', tab_det[3].text.lower()]})
                elif tab_det[3].text == '\xa0':
                    dict.update({tab_det[0].text.lower(): [tab_det[1].text.lower(), tab_det[2].text.lower(), '']})
                else:
                    dict.update({tab_det[0].text.lower(): [tab_det[1].text.lower(), tab_det[2].text.lower(), tab_det[3].text.lower()]})

    return dict

"""
Extracting file as json file
"""
def export_json(dicts, file):
    # open the file "filename" in write ("w") mode
    with open(file,"w") as fp:
        json.dump(dicts, fp, indent=4, sort_keys=True)

"""
Reading json data
"""
def read_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

"""
Extracting as CSV
"""
def export_csv(dict, csvfile):
    with open(csvfile, 'w') as csvfile:
        w = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        for key, value in dict.items():
            w.writerow([key])
            w.writerow([value])

def open_json(file):
    json_data=open(file).read()
    data = json.loads(json_data)
    print(data)

def main():
    list = extract_details()
    export_json(list,"jsonfile.json")
    """with open("jsonfile.json","w") as fp:
        json.dump(list, fp, indent=4, sort_keys=True)"""

if __name__ == "__main__":
    main()
