import csv
import requests

#
model_list = ['Aston Martin', 'Audi', 'BMW', 'Bentley', 'Bugatti', 'DC', 'Datsun', 'Ferrari', 'Fiat', 'Force', 'Ford',
              'Honda', 'Hyundai', 'ICML', 'Isuzu', 'Jaguar', 'Jeep', 'Lamborghini', 'Land Rover', 'Lexus', 'Mahindra',
              'Maruti', 'Maserati', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Porsche', 'Premier', 'Renault',
              'Rolls-Royce', 'Skoda', 'Tata', 'Toyota', 'Volkswagen', 'Volvo']
model_list = sorted(model_list)
TEST_KEY = 'Ahmedabad'
# model_list = ['Aston Martin']
TEST_CITY_ID = 51
TEST_URL = "https://www.cardekho.com/api/v1/dealer/dealerList?lang_code=en&business_unit=car&country_code=in&_format=json&cityId={CITY_ID}&connectoid=58367c42-d25f-d977-a43c-912c888df744&sessionid=4cb5f93029e79c96180b6b56f4904208&lang_code=en&regionId=0&otherinfo=all&url=%2F{MODEL}%2F{CITY_KEY}%2Fcardealers"""
URL = "https://www.cardekho.com/api/v1/dealer/dealerList?lang_code=en&business_unit=car&country_code=in&_format=json&cityId={CITY_ID}&connectoid=58367c42-d25f-d977-a43c-912c888df744&sessionid=4cb5f93029e79c96180b6b56f4904208&lang_code=en&regionId=0&otherinfo=all&url={END_POINT}"""

count = 0
ddata = []
highest = {}
is_first = True

for model in model_list:
    formatted_model = model.replace(' ', '_')
    url = TEST_URL.format(CITY_ID=TEST_CITY_ID, MODEL=formatted_model, CITY_KEY=TEST_KEY)
    r = requests.get(url)
    request_data = r.json()
    for item in request_data['data']['cities']['items']:
        ddata = []
        r1 = requests.get(URL.format(CITY_ID=item['id'], END_POINT=item["url"].replace('/', '%2F')))
        for dealers in r1.json()['data'].get('dealers', {}).get('items', []):
            for dealer in dealers.get('items'):
                if dealer.get('contactDetails'):
                    row = [dealer.get('brand'), dealer.get('city'), dealer.get('name'), dealer.get('latitude'),
                           dealer.get('longitude'), dealer['contactDetails'][0].get('phone'),
                           dealer['contactDetails'][0].get('fax'), dealer['contactDetails'][0].get('email'),
                           dealer['contactDetails'][0].get('address'), ]
                else:
                    row = [dealer.get('brand'), dealer.get('city'), dealer.get('name'), dealer.get('latitude'),
                           dealer.get('longitude'), ]
                ddata.append(row)
        with open('data.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            if is_first:
                header_row = ['Brand Name', 'City', 'Name', 'Latitude', 'Longitude', 'Phone', 'Fax', 'Email',
                              'Address']
                is_first = False
                writer.writerow(header_row)
            writer.writerows(ddata)
    print(f'{model} Completed')
csvFile.close()
print(highest)
print(ddata)
print(len(ddata))
