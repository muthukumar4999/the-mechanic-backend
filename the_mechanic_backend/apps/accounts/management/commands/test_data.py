from django.core.management.base import BaseCommand
from django.utils import timezone

from the_mechanic_backend.apps.service.models import ServiceType, Service, SubService, GeneralService
from the_mechanic_backend.apps.stock.models import BrandModel, Brand


class Command(BaseCommand):
    help = 'Create Test Data'

    DATA = {'Aprilia': ['SR 150'],
            'Bajaj': ['Avenger 150', 'Avenger 180', 'Avenger 200 DTSi', 'Avenger 220 DTSi', 'Avenger Cruise 220',
                      'Avenger Street 150', 'Avenger Street 220', 'Bajaj NS 200', 'Bajaj Pulsar RS 200', 'Boxer',
                      'Caliber 115', 'CT 100', 'Discover', 'Discover 100', 'Discover 100 CC', 'Discover 125 CC',
                      'Discover 125 ST', 'Discover 150S', 'Discover DTSi', 'Exceed', 'F 150', 'Kristal',
                      'New Discover 125', 'Platina', 'Platina 100 ES', 'Pulsar', 'Pulsar 135', 'Pulsar 150',
                      'Pulsar 150 NS', 'Pulsar 180', 'Pulsar 180 NS', 'Pulsar 200', 'Pulsar 200 AS', 'Pulsar 200 FI',
                      'Pulsar 200 NS', 'Pulsar 200 SS', 'Pulsar 220', 'Pulsar 250 CC', 'Pulsar 300 CC', 'Pulsar 350 NS',
                      'Pulsar 375', 'Pulsar CS400', 'Pulsar RS 200', 'Pulsar SS400', 'V15', 'Wave', 'XCD 125',
                      'XCD 150', 'Other'], 'Harley Davidson': ['Street 750'],
            'Hero': ['Achiever', 'Dare', 'Dash', 'Duet', 'Glamour 125', 'Glamour Programmed FI', 'Hastur',
                     'Hero EBR 250', 'HF-Dawn', 'HF-Deluxe', 'HF-Deluxe Eco', 'Hunk 150 CC', 'HX 250R', 'Ignitor',
                     'Impulse', 'Impulse 250', 'iON', 'iSMART', 'Karizma', 'Karizma', 'Karizma ZMR', 'Karizma ZMR 250',
                     'Karizma ZMR FI', 'Leap', 'Maestro', 'Maestro 125', 'Passion Plus', 'Passion Pro 100',
                     'Passion Pro TR', 'Passion XPRO', 'Pleasure 100', 'Pleasure IBS', 'RNT Diesel', 'SimplEcity',
                     'Splendor iSMART', 'Splendor NXG 100', 'Splendor Plus 100', 'Splendor Pro 100',
                     'Splendor Pro Classic', 'Super Splendor 125', 'Super Splendor Classic', 'Xtreme', 'Xtreme Sports',
                     'Zir', 'Other'],
            'Hero Moto Corp': ['Ambition', 'CBZ', 'CBZ Extreme', 'CBZ Extreme sports 150', 'CD 100', 'CD Dawn',
                               'CD Deluxe', 'Dawn', 'Deluxe', 'Glamour', 'Glamour Fi', 'Hunk', 'Karizma', 'Karizma ZMR',
                               'Passion', 'Passion Plus', 'Passion Pro', 'Pleasure', 'Splendor', 'Splendor NXG',
                               'Splendor Plus', 'Splendor Pro', 'Super Splendor', 'Other'],
            'Honda': [' CB Hornet 160R', 'Activa', 'Activa 125', 'Activa 3g', 'Activa i', 'Aviator', 'CB Shine',
                      'CB Trigger', 'CB Twister', 'CB Unicorn', 'CB Unicorn 160', 'CBF Stunner', 'CBR 120', 'CBR 150',
                      'CBR 250', 'CBR 250R', 'CD110 Dream', 'Dazzler', 'Dio', 'Dream Neo', 'Dream Yuga', 'Eterno',
                      'Neo', 'Neo', 'Shine', 'Other'], 'Kawasaki': ['Ninja', 'Ninja', 'Ninja 300'],
            'Kinetic': ['4S', 'Blaze', 'Boss', 'Flyte', 'K4', 'Stryker', 'SYM', 'V2', 'Velocity', 'Zing', 'Other'],
            'KTM': ['390 Adventure', '450 EXC', 'Duke 125', 'Duke 125 CC', 'Duke 200', 'Duke 200 CC', 'Duke 250',
                    'Duke 390 ', 'Duke 390 ABS', 'Duke 690', 'RC 125', 'RC 200', 'RC 390', 'RC25', 'Super Duke 990',
                    'Other'], 'LML': ['Freedom', 'LML NV', 'Star 200', 'Star Euro 150', 'Other'],
            'Mahindra': ['Arro', 'Centuro', 'Centuro 01-D', 'Duro', 'Duro DZ', 'Flyte', 'GenZe', 'Gusto', 'jcMoto',
                         'Kine', 'Mojo', 'Mojo', 'Mojo 300', 'Pantero', 'Rodeo', 'Rodeo UZO 125', 'Scrambler', 'Other'],
            'Piaggio': ['Aprilia RSV4', 'Liberty', 'Vespa', 'Vespa 946', 'Vespa LX 125', 'Vespa S', 'Vespa Sport',
                        'Other'],
            'Royal Enfield': ['Bullet 350 Twinspark', 'Bullet 500', 'Bullet 500 EFI', 'Bullet Classic',
                              'Bullet Electra Twinspark', 'Café Racer 500', 'Classic 350', 'Classic 500',
                              'Classic Battle Green', 'Classic Chrome', 'Classic Desert Storm', 'Continental GT',
                              'Electra', 'Fury 500', 'Himalayan ', 'Machismo 350', 'Thunderbird 350', 'Thunderbird 500',
                              'Other'],
            'Suzuki': ['Access', 'Access 125', 'Bandit 1250SA', 'Fiero', 'Gixer', 'Gladius 650', 'GS 150 R', 'GSR250F',
                       'GSX 150 R', 'GSX-R1000', 'GW 250', 'Hayate', 'Inazuma 250', 'Intruder', 'Lets', 'Samurai',
                       'Slingshot Plus', 'Swish 125', 'V-Storm', 'ZEUS', 'Other'],
            'TVS': ['Apache', 'Apache 180', 'Apache 220 CC', 'Apache 250 CC', 'Apache RTR', 'Apache RTR 160',
                    'Apache RTR 180', 'Apache RTR 200 CC', 'Apache RTR 300 FX', 'Centra', 'Draken', 'Fiero', 'Flame',
                    'Flame SR 125', 'Graphite', 'Heavy Duty Super XL', 'Jive', 'Jupiter', 'Max 100', 'Max 125',
                    'Max 4R', 'Other', 'Phoenix', 'Phoenix', 'Qube', 'Radeon', 'Rockz', 'Scooty', 'Scooty Pep',
                    'Scooty Pep Plus', 'Scooty Streak', 'Scooty Zest', 'Sport', 'Star', 'Star City', 'Star City Plus',
                    'Star Sport', 'Victor', 'Wego', 'Wego', 'Other'],
            'Yamaha': ['Crux', 'Cygnus Alpha', 'Cygnus X 125', 'Delight', 'Enticer', 'Fascino', 'Fazer', 'Fazer 250 CC',
                       'Fazer8', 'FZ 16', 'FZ 16 V2', 'FZ 2', 'FZ S', 'FZ-1', 'FZ-S', 'Gladiator', 'MT 125', 'MT 25',
                       'MT-01', 'Neo', 'Nozza Grande', 'R125', 'R15', 'R25', 'R6', 'Ray', 'Ray 125 CC', 'Ray Z',
                       'RD350', 'RX 100', 'RX 100', 'RX 135', 'Saluto', 'SS 125', 'SZ', 'SZ-R', 'SZ-RR', 'SZ-S', 'SZX',
                       'YBR', 'YBR 125', 'YBX', 'YZF R15', 'Other'], 'Other': ['Rajdoot 350', 'Yezdi', 'Other']}

    SERVICE_TYPE = [{'name': 'General Service', 'is_general': True, 'has_sub': False, 'subs': [],
                     'general': ['Head Light', 'Danger Light', 'FR- Break Light', 'RR- Break Light',
                                 'Battery', 'Horn', 'IND - Buzzer', 'Self start', 'Tank Bag',
                                 'Mat', 'Indicator - Front', 'Indicator - Rear', 'Engine Oil',
                                 'Fuel', 'Fork Oil', 'Forkoil Leak', 'Coneset', 'Stay Bush',
                                 'Break Shoe - FR', 'Break Shoe - RR', 'Speedo Meter - Worm',
                                 'Speedo Meter - Cable']},
                    {'name': 'Repair Job', 'is_general': False, 'has_sub': False, 'subs': [], 'general': []},
                    {'name': 'Premium Service', 'is_general': False, 'has_sub': False, 'subs': [], 'general': []},
                    {'name': 'Water Service', 'is_general': False, 'has_sub': False, 'subs': [], 'general': []},
                    {'name': 'Other Service', 'is_general': False, 'has_sub': True,
                     'subs': ['Lath', 'Welding', 'Electrical', 'Fiber Moulding', 'S C / T B',
                              'S/M Repair', 'Tyre'], 'general': []},
                    ]

    def handle(self, *args, **kwargs):
        self.add_vehicle_details()
        self.add_service_type()

    def add_vehicle_details(self):
        Brand.objects.all().delete()
        for key, value in self.DATA.items():
            brand = Brand.objects.filter(name=key)
            if not brand:
                brand = Brand(name=key)
                brand.save()
            for item in value:
                brand_model = BrandModel(brand=brand,
                                         model_name=item)
                brand_model.save()

    def add_service_type(self):
        ServiceType.objects.all().delete()
        GeneralService.objects.all().delete()
        for item in self.SERVICE_TYPE:
            service = ServiceType(service_name=item['name'],
                                  is_general=item['is_general'],
                                  has_sub=item['has_sub'])
            service.save()
            for sub in item['subs']:
                SubService(service=service,
                           sub_service_name=sub).save()

            for check_list in item['general']:
                GeneralService(check_list=check_list).save()
