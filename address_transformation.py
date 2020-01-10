import requests
import json
import csv
import time
from tqdm import *

def addresses_from_csv(path=None, idColumn=None, addrColumn=None):
        
    addresses = []

    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
        first_row = next(reader)
        for row in reader:
            addresses.append([row[idColumn],row[addrColumn]])
            # print(row[idColumn], row[addrColumn])
            
    return addresses
  
# Get addresses from CSV
addresses = addresses_from_csv(path='input.csv', idColumn=0, addrColumn=1)
#print(addresses)

# Set Google Maps API key
api_key = 'YOUR_API_KEY'

# Initialize array for transformed addresses
transformed = []
transformed.append(['ID', 'Country', 'Post code', 'City', 'Street', 'Number'])

for query in tqdm(addresses):
    
    # API call, storing information as JSON
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + query[1] + '&lang=en&key=' + api_key
    r = requests.get(url)
    data = r.json()
    #print(data)
    
    # clear all values to avoid appending values from previous iterations a second time
    number = street = country = postal_code = city = '' 
    
    if data['status'] == 'ZERO_RESULTS':
        transformed.append([query[0], 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
        print(url)
        print(data)
    else:
        # looping over address components in JSON
        for component in data['results'][0]['address_components']:
            if 'street_number' in component['types']:
                number = component['long_name']
            elif 'route' in component['types']:
                street = component['long_name']
            elif 'country' in component['types']:
                country = component['long_name']
            elif 'postal_code' in component['types']:
                postal_code = component['long_name']
            elif 'locality' in component['types']:
                city = component['long_name']
            elif 'postal_town' in component['types']:
                city = component['long_name']
            else:
                continue

        transformed.append([query[0], country, postal_code, city, street, number])
    
with open('output_' + time.strftime('%Y%m%d-%H%M%S') + '.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_ALL, quotechar='"')
    for row in transformed:
        writer.writerow(row)

print('Done')