#!/usr/bin/python3
import requests
import json
import argparse
import csv


def call_api(title):
    payload = {'address': title.replace(' ','+'), 'key': 'AIzaSyDkRfLR-E9TV5xHHwqFwRcs58zTs2eyE50'}
    # Using REST    
    print(title + "....")
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json",
        headers={
            "Accept": "application/json"
        },
        params=payload
    )
    if r.status_code != 200:
        print(f"Error. Return code={r.status_code}")
    # Serialize json mesage
    data = json.loads(r.text)
    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']

    d = {}
    d['title'] = title
    d['latitude'] = lat
    d['longitude'] = lng
    return d

def main():
    # parser = argparse.ArgumentParser(description='Produce data to kafka topic.')
    # parser.add_argument('--time', type=int, dest='runtime', default=300, help='total runtime in seconds')

    # args = parser.parse_args()
    places = []
    with open('in.csv','r', newline='\n') as f:
        reader = csv.reader(f, delimiter=',')
        #skip header line
        next(reader)
        places = list(reader)

    print(places)
    print("------------------------")
    f.close()

    with open('places.csv', 'w', newline='\n') as outfile:
        fieldnames = ['title', 'latitude', 'longitude']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for t in places: 
            writer.writerow(call_api(t[0]))


if __name__ == "__main__":
    main()