from airtable import Airtable

air_table = Airtable('appneUKQmR3Sjrr5B', 'Timeseries', 'keytS1JgO9Fd3zvhG')
dir(air_table)
air_table.get_all()

import requests
import csv
post_url = 'https://api.airtable.com/v0/appneUKQmR3Sjrr5B/CSVImport'
post_headers = {
    'Authorization': 'Bearer ' + 'keytS1JgO9Fd3zvhG',
    'Content-Type': 'application/json'
}
f = open('data/study.csv')
csv_f = csv.reader(f)
for row in csv_f:
    name = row[0]
    number = row[1]
    role = row[2]
    data = {
    "fields": {
        "Field1": name,
        "Field2": number,
        "Field3": role
        }
    }
    print(post_url)
    print(data)
    post_airtable_request = requests.post(post_url, headers=post_headers, json=data)
    print(post_airtable_request.status_code)

