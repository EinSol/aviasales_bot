empty_wishlist_text='your wishlist is empty :('
hotel_representation_text = '''Hotel: {}
Town: {}
Stars: {}
Start price: {}
'''
tour_representation_text = '''Arrival date: {}
Nights: {}
Room: {}
Food: {}
Price: {}
'''
test = [{'hotel_name': 'Semoris Hotel',
  'stars': '3',
  'start_price': '726грн.',
  'tours': [{'arrival_date': '18.08.2021',
             'food': 'BB',
             'nights': '7',
             'price': '47\xa0726грн.',
             'room': 'STANDARD ROOM/DBL'}],
  'town': 'Сиде центр'},
 {'hotel_name': 'Club Agon Hotel Kemer (ex. Infinity Hotel Kemer)',
  'stars': '3',
  'start_price': '726грн.',
  'tours': [{'arrival_date': '18.08.2021',
             'food': 'BB',
             'nights': '7',
             'price': '47\xa0726грн.',
             'room': 'Standard/DBL'}],
  'town': 'Кемер центр'},
 {'hotel_name': 'Himeros Beach Hotel',
  'stars': '3',
  'start_price': '226грн.',
  'tours': [{'arrival_date': '18.08.2021',
             'food': 'AI',
             'nights': '7',
             'price': '48\xa0226грн.',
             'room': 'STANDARD ROOM/DBL'}],
  'town': 'Кемер центр'},
 {'hotel_name': 'Ozgurhan Hotel',
  'stars': '3',
  'start_price': '226грн.',
  'tours': [{'arrival_date': '18.08.2021',
             'food': 'ROOM ONLY',
             'nights': '7',
             'price': '48\xa0226грн.',
             'room': 'STANDARD ROOM/DBL'}],
  'town': 'Сиде центр'},
 {'hotel_name': 'Beldibi Hotel',
  'stars': '3',
  'start_price': '226грн.',
  'tours': [{'arrival_date': '18.08.2021',
             'food': 'AI',
             'nights': '7',
             'price': '48\xa0226грн.',
             'room': 'STANDARD ROOM/DBL'}],
  'town': 'Бельдиби'},
 {'hotel_name': 'Amanda Hotel',
  'stars': 'u',
  'start_price': '226грн.',
  'tours': [{'arrival_date': '18.08.2021',
             'food': 'BB',
             'nights': '7',
             'price': '48\xa0226грн.',
             'room': 'STANDARD ROOM/DBL'}],
  'town': 'Кемер центр'},
 {'hotel_name': 'Kleopatra Smile Hotel',
  'stars': '3',
  'start_price': '726грн.',
  'tours': [{'arrival_date': '18.08.2021',
             'food': 'BB',
             'nights': '7',
             'price': '48\xa0726грн.',
             'room': 'STANDARD ROOM/DBL'}],
  'town': 'Алания'},
 {'hotel_name': 'Vella Beach Hotel',
  'stars': '3',
  'start_price': '226грн.',
  'tours': [{'arrival_date': '18.08.2021',
             'food': 'AI',
             'nights': '7',
             'price': '49\xa0226грн.',
             'room': 'STANDARD ROOM/DBL'}],
  'town': 'Алания Обакой'},
 {'hotel_name': 'Club Herakles Hotel',
  'stars': '3',
  'start_price': '226грн.',
  'tours': [{'arrival_date': '18.08.2021',
             'food': 'AI',
             'nights': '7',
             'price': '49\xa0226грн.',
             'room': 'STANDARD ROOM/DBL'}],
  'town': 'Кемер центр'},
 ]

wishlist_representation_text = '''Hotel: {}
Town: {}
Arrival date: {}
Nights: {}
Stars: {}
Room: {}
Food: {}
Price: {}
'''

add_item_text='add something to wishlist.'
enter_name_text='enter your name and surname:'
incorrect_name_text='invalid name, try again.'
invalid_phone_text='invalid phone number, try again.'
enter_phone_text='enter your phone number (start with +38 etc.):'
choose_messager_text='choose messager you want to get in touch'
user_data_text='''your application:
name: {}
phone: {}
messager: {}'''
uncomplete_formular_text='You didnt choose date, destination country or departure city.'
no_tours_text='Any available tours :('
