#!/usr/bin/python3
import os
import requests
import json
import csv
import googlemaps

gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_MAPS_API_KEY"))

def call_api(title):
    geocode_result = gmaps.geocode(title)
    data = geocode_result[0]
    lat = data['geometry']['location']['lat']
    lng = data['geometry']['location']['lng']

    d = {}
    d['title'] = title
    d['latitude'] = lat
    d['longitude'] = lng
    return d

def main():
    places = []
    with open('in.csv','r', newline='\n') as f:
        reader = csv.reader(f, delimiter=',')
        #skip header line
        next(reader)
        places = list(reader)

    print(places)
    print("------------------------")
    f.close()

    print("starting geocoding now")
    with open('places.csv', 'w', newline='\n') as outfile:
        fieldnames = ['title', 'latitude', 'longitude']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for t in places: 
            writer.writerow(call_api(t[0]))
    print("finished geocoding!")


if __name__ == "__main__":
    main()