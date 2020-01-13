import requests
import csv
import time
from tqdm import *

# Settings
google_maps_api_key = '__REPLACE_GOOGLE_API_KEY_HERE__'
input_path = 'input.csv'
id_column = 0
addr_column = 1
reader_delimiter = ';'
reader_quoting = csv.QUOTE_NONE

# Get all addresses from CSV
addresses = []
with open(input_path, 'r') as f:
    reader = csv.reader(f, delimiter=reader_delimiter, quoting=reader_quoting)

    # Check and ignore first line
    first_row = next(reader)
    if first_row[0] != 'id':
        print('Warning: First line is ignored, it should have value of "id;address"')

    for row in reader:
        addresses.append([row[id_column], row[addr_column]])


# Open files for writing
time_str = time.strftime('%Y%m%d-%H%M%S')
file_found = open('found_' + time_str + '.csv', 'w', newline='\n', encoding='utf-8')
file_failed = open('failed_' + time_str + '.csv', 'w', newline='\n', encoding='utf-8')

# Initiate csv writer
writer_found = csv.writer(file_found, delimiter=';', quoting=csv.QUOTE_ALL, quotechar='"', escapechar='\\')
writer_failed = csv.writer(file_failed, delimiter=';', quoting=csv.QUOTE_ALL, quotechar='"', escapechar='\\')

# Set headers
writer_found.writerow(['ID', 'Street', 'Street (Short)', 'Number', 'Post code', 'City', 'State', 'State (Short)', 'Country'])
writer_failed.writerow(['ID', 'Failure Reason', 'Address'])


# Loop through addresses, create request and write to files
fails_count = 0
success_count = 0
total_addresses = len(addresses)

for query in tqdm(addresses):
    if len(query) != 2:
        reason = 'Expected two columns but found ' + str(len(query))
        writer_failed.writerow([query[0], reason, ''])
        file_failed.flush()
        print('Skipping ' + query[0] + ' ' + reason)
        fails_count += 1

    try:
        # API call, storing information as JSON
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + query[1] + '&lang=en&key=' + google_maps_api_key
        r = requests.get(url, timeout=15)
        data = r.json()

        # clear all values to avoid appending values from previous iterations a second time
        number = street = country = postal_code = city = street_short = state = state_short = ''

        if data['status'] == 'ZERO_RESULTS':
            writer_failed.writerow([query[0], 'ZERO_RESULT', query[1]])
            print('No result found for #' + query[0])
            file_failed.flush()
            print(url)
            print(data)
            fails_count += 1
        else:
            # looping over address components in JSON
            for component in data['results'][0]['address_components']:
                if 'street_number' in component['types']:
                    number = component['long_name']
                elif 'route' in component['types']:
                    street = component['long_name']
                    street_short = component['short_name']
                elif 'country' in component['types']:
                    country = component['long_name']
                elif 'administrative_area_level_1' in component['types']:
                    state = component['long_name']
                    state_short = component['short_name']
                elif 'postal_code' in component['types']:
                    postal_code = component['long_name']
                elif 'locality' in component['types']:
                    city = component['long_name']
                elif 'postal_town' in component['types']:
                    city = component['long_name']
                else:
                    continue
            writer_found.writerow([query[0], street, street_short, number, postal_code, city, state, state_short, country])
            file_found.flush()
            success_count += 1
    except:
        writer_failed.writerow([query[0], 'Exception', query[1]])
        print('Exception while trying to get #' + query[0])
        file_failed.flush()
        fails_count += 1

print('############')
print('# Found: ' + str(success_count))
print('# Failed: ' + str(fails_count))
print('# Total: ' + str(total_addresses))
print('############')
print('Done')
