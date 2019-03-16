import json

import requests
BRANDS = [{"Id": 23, "Make": "Aprilia", "Active": False}, {"Id": 2, "Make": "Bajaj", "Active": False},
              {"Id": 22, "Make": "Harley Davidson", "Active": False}, {"Id": 1, "Make": "Hero", "Active": False},
              {"Id": 3, "Make": "Hero Moto Corp", "Active": False}, {"Id": 12, "Make": "Honda", "Active": False},
              {"Id": 19, "Make": "Kawasaki", "Active": False}, {"Id": 13, "Make": "Kinetic", "Active": False},
              {"Id": 4, "Make": "KTM", "Active": False}, {"Id": 5, "Make": "LML", "Active": False},
              {"Id": 6, "Make": "Mahindra", "Active": False}, {"Id": 7, "Make": "Piaggio", "Active": False},
              {"Id": 8, "Make": "Royal Enfield", "Active": False}, {"Id": 9, "Make": "Suzuki", "Active": False},
              {"Id": 10, "Make": "TVS", "Active": False}, {"Id": 11, "Make": "Yamaha", "Active": False},
              {"Id": 14, "Make": "Other", "Active": False}]


data = {}


for item in BRANDS:
    make = item['Make']
    data[make] = []
    url = f"http://gaadi360.com/handlers/vehicleModels.ashx?makeId={item['Id']}"
    for model in requests.get(url).json():
        model_name = model['model']
        data[make].append(model_name)

print(data)
