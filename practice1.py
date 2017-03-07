#import statements for all necessary components
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

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

def extract_details():
    header = []
    title = soup.find_all('span', {'class': 'style4'})
    for i in title:
        header.append(i.text)
    dict = {}
    table = soup.find_all('table')
    product_name = []
    room_temp = []
    refridg = []
    freezer = []

    for tag in table:
        for tr in tag.find_all('tr'):
            tab_det = tr.find_all('td')
            if len(tab_det) == 4:
                if tab_det[1].text == '\xa0':
                    dict.update({tab_det[0].text: ['', tab_det[2].text, tab_det[3].text]})
                elif tab_det[2].text == '\xa0':
                    dict.update({tab_det[0].text: [tab_det[1].text, '', tab_det[3].text]})
                elif tab_det[3].text == '\xa0':
                    dict.update({tab_det[0].text: [tab_det[1].text, tab_det[2].text, '']})
                else:
                    dict.update({tab_det[0].text: [tab_det[1].text, tab_det[2].text, tab_det[3].text]})

    #df = pd.DataFrame(product_name, columns=['header'])
    #df['Room Temperature'] = room_temp
    #df['Refrigerator'] = refridg
    #df['Freezer'] = freezer

    #print(df)
    return dict

def export_json(dict, file):
    # open the file "filename" in write ("w") mode
    with open(file, "w") as jsonfile:
        # just an example dictionary to be dumped into "filename"
        # dumps "output" encoded in the JSON format into "filename"
        json.dump(dict, jsonfile)
        jsonfile.close()

def export_csv(dict, csvfile):
    with open(csvfile, 'w') as csvfile:
        w = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        #w.writeheader()
        #w.writerow(dict)
        #print(dict)
        #Test to make sure dictionary has necessary items
        for key, value in dict.items():
            w.writerow([key])
            w.writerow([value])



def main():
    list = extract_details()
    export_csv(list, csvfile)
    export_csv(list, "jsonfile.json")

if __name__ == "__main__":
    main()
