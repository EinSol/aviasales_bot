import telegram.error
from telegram.ext import (MessageHandler, Filters, CallbackContext, CallbackQueryHandler,
                          ConversationHandler, CommandHandler, )
from telegram import (Update, ParseMode)
from search_screen.texts import (welcome_text, wrong_input_text, wrong_date_text,
                                 country_list, city_list, enter_destination_text,
                                 enter_departure_text, enter_date_text, old_date_text, adults_text,
                                 kids_text, nights_amount_text, request_template_text, stars_text,
                                 food_text, incorrect_range_date_text, )
from datetime import datetime
from pprint import pprint
from keyboards import (adults_kb, kids_kb, stars_kb, food_list, food_kb,
                       search_reply_kb, search_reply_buttons)
from result_screen.handlers import result_conversation_handler
from decouple import config

SEARCH_FUNCTIONS, DESTINATION_FUNCTION, \
DEPARTURE_FUNCTION, DATE_FUNCTION, STARS_FUNCTION, \
FOOD_FUNCTION, ADULTS_FUNCTION, KIDS_FUNCTION, NIGHTS_FUNCTION, \
    = range(9)


def start_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    username = update.message.chat.username
    context.bot.send_message(chat_id=cid,
                             text=welcome_text.format(username),
                             reply_markup=search_reply_kb)
    request_template = {'destination_country': None,
                        'departure_city': None,
                        'min_nights': '7',
                        'max_nights': '10',
                        'date': '',
                        'adults': '2',
                        'kids': '0',
                        'stars': [],
                        'food': []
                        }

    context.chat_data.update({'search_request': request_template})
    context.chat_data['temporary_ids'] = []

    payload = {'message_id': 0,
               'current_index': 0,
               'number_of_items': 0,
               'wishlist_info': []}
    context.chat_data['wishlist'] = payload
    context.chat_data['application'] = {'name': '',
                                        'phone': '',
                                        'messager': ''}

    return SEARCH_FUNCTIONS


start_handler = CommandHandler(command='start',
                               callback=start_callback,
                               pass_chat_data=True,
                               filters=~Filters.chat(config('TEST_ADMIN_ID')))


def destination_country_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    country_list_text = ''.join([f'{index+1}. {text}\n' for index, text in enumerate(country_list)])
    update.message.reply_text(country_list_text)
    update.message.reply_text(enter_destination_text)

    return DESTINATION_FUNCTION


destination_country_handler = MessageHandler(callback=destination_country_callback,
                                             pass_chat_data=True,
                                             filters=Filters.regex('^{}$'.format(search_reply_buttons[0][0])))


def validate_destination_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text

    try:
        q = int(q) - 1
        if 0 > q or q > len(country_list) - 1:
            raise ValueError
    except Exception as e:
        update.message.reply_text(wrong_input_text)
        return

    search_request = context.chat_data['search_request']
    pprint(search_request)
    search_request['destination_country'] = q
    update.message.reply_text(f'Your country code: {q + 1}')

    return SEARCH_FUNCTIONS


validate_destination_handler = MessageHandler(callback=validate_destination_callback,
                                              pass_chat_data=True,
                                              filters=Filters.text)


def departure_city_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    city_list_text = ''.join([f'{index+1}. {text}\n' for index, text in enumerate(city_list)])
    update.message.reply_text(city_list_text)
    update.message.reply_text(enter_departure_text)
    return DEPARTURE_FUNCTION


departure_city_handler = MessageHandler(callback=departure_city_callback,
                                        pass_chat_data=True,
                                        filters=Filters.regex('^{}$'.format(search_reply_buttons[0][1])))


def validate_departure_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text

    try:
        q = int(q) - 1
        if 0 > q or q > len(city_list) - 1:
            raise ValueError
    except Exception as e:
        print(e)
        update.message.reply_text(wrong_input_text)
        return

    search_request = context.chat_data['search_request']
    pprint(search_request)
    search_request['departure_city'] = q

    update.message.reply_text(f'Your city code: {q + 1}')
    return SEARCH_FUNCTIONS


validate_departure_handler = MessageHandler(callback=validate_departure_callback,
                                            pass_chat_data=True,
                                            filters=Filters.text)


def date_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    update.message.reply_text(enter_date_text)
    return DATE_FUNCTION


date_handler = MessageHandler(callback=date_callback,
                              pass_chat_data=True,
                              filters=Filters.regex('^{}$'.format(search_reply_buttons[0][2])))


def validate_date_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = "".join(update.message.text.split())
    date_format = '%d.%m.%Y'

    try:
        dates = q.split('-')
        if len(dates) > 2:
            return ValueError
        date1 = datetime.strptime(dates[0], date_format).date()
        date2 = datetime.strptime(dates[1], date_format).date()
        if date1 < datetime.today().date():
            update.message.reply_text(old_date_text)
            return

        if date2 < date1:
            update.message.reply_text(incorrect_range_date_text)
            return

    except Exception as e:
        print(e)
        update.message.reply_text(wrong_date_text)
        return

    search_request = context.chat_data['search_request']
    pprint(search_request)
    search_request['date'] = q
    context.chat_data.update({'search_request': search_request})

    update.message.reply_text(f'Your date: {q}')
    return SEARCH_FUNCTIONS


validate_date_handler = MessageHandler(callback=validate_date_callback,
                                       pass_chat_data=True,
                                       filters=Filters.text)


def hotel_stars_callback(update: Update, context: CallbackContext) -> int:
    cid = update.effective_chat.id
    star_text_options = [''] * 5
    message = context.bot.send_message(chat_id=cid,
                                       text=stars_text.format(*star_text_options),
                                       reply_markup=stars_kb)

    payload = {
        'hotel_stars_keyboard_message_id': message.message_id,
        'stars': []
    }
    context.chat_data.update(payload)
    return STARS_FUNCTION


hotel_stars_handler = CommandHandler(command='stars',
                                     callback=hotel_stars_callback,
                                     pass_chat_data=True,
                                     )


def add_hotel_stars_callback(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    cid = update.effective_chat.id
    star = int(update.callback_query.data.split(':')[-1])
    stars = context.chat_data.get('stars', [])
    mid = context.chat_data.get('hotel_stars_keyboard_message_id')
    star_text_options = [''] * 5

    if star in stars:
        stars.remove(star)
        query.answer(text=f'{star} is removed')
    else:
        stars.append(star)
        query.answer(text=f'{star} is added')

    for a in stars:
        star_text_options[a] = '#'

    context.bot.edit_message_text(chat_id=cid,
                                  message_id=mid,
                                  text=stars_text.format(*star_text_options),
                                  reply_markup=stars_kb,
                                  parse_mode=ParseMode.HTML)

    context.chat_data.update({'stars': stars})

    return STARS_FUNCTION


add_hotel_stars_handler = CallbackQueryHandler(callback=add_hotel_stars_callback,
                                               pattern=r'stars:\d',
                                               pass_chat_data=True)


def submit_hotel_stars_callback(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer('submitted!')
    cid = update.effective_chat.id
    stars = context.chat_data.get('stars', [])
    mid = context.chat_data.get('hotel_stars_keyboard_message_id')
    star_text_options = [''] * 5

    for a in stars:
        star_text_options[a] = '#'

    context.bot.edit_message_text(chat_id=cid,
                                  message_id=mid,
                                  text=stars_text.format(*star_text_options),
                                  parse_mode=ParseMode.HTML)
    search_request = context.chat_data['search_request']
    search_request['stars'] = stars
    pprint(search_request)
    context.chat_data.update({'search_request': search_request})
    return SEARCH_FUNCTIONS


submit_hotel_stars_handler = CallbackQueryHandler(callback=submit_hotel_stars_callback,
                                                  pattern='stars:submit',
                                                  pass_chat_data=True)


def hotel_food_callback(update: Update, context: CallbackContext) -> int:
    cid = update.effective_chat.id
    star_text_options = [''] * 6
    message = context.bot.send_message(chat_id=cid,
                                       text=food_text.format(*star_text_options),
                                       reply_markup=food_kb)

    payload = {
        'hotel_food_keyboard_message_id': message.message_id,
        'food': []
    }
    context.chat_data.update(payload)
    return FOOD_FUNCTION


hotel_food_handler = CommandHandler(command='food',
                                    callback=hotel_food_callback,
                                    pass_chat_data=True,
                                    )


def add_hotel_food_callback(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    cid = update.effective_chat.id
    meal = int(update.callback_query.data.split(':')[-1])
    food = context.chat_data.get('food', [])
    mid = context.chat_data.get('hotel_food_keyboard_message_id')
    food_text_options = [''] * 6

    if meal in food:
        food.remove(meal)
        query.answer(text=f'{food_list[meal]} is removed')
    else:
        food.append(meal)
        query.answer(text=f'{food_list[meal]} is added')

    for a in food:
        food_text_options[a] = '#'

    context.bot.edit_message_text(chat_id=cid,
                                  message_id=mid,
                                  text=food_text.format(*food_text_options),
                                  reply_markup=food_kb,
                                  parse_mode=ParseMode.HTML)

    context.chat_data.update({'food': food})

    return FOOD_FUNCTION


add_hotel_food_handler = CallbackQueryHandler(callback=add_hotel_food_callback,
                                              pattern=r'food:\d',
                                              pass_chat_data=True)


def submit_hotel_food_callback(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer('submitted!')
    cid = update.effective_chat.id
    food = context.chat_data.get('food', [])
    mid = context.chat_data.get('hotel_food_keyboard_message_id')
    food_text_options = [''] * 6

    for a in food:
        food_text_options[a] = '#'

    context.bot.edit_message_text(chat_id=cid,
                                  message_id=mid,
                                  text=food_text.format(*food_text_options),
                                  parse_mode=ParseMode.HTML)
    search_request = context.chat_data['search_request']
    search_request['food'] = food
    pprint(search_request)
    context.chat_data.update({'search_request': search_request})
    return SEARCH_FUNCTIONS


submit_hotel_food_handler = CallbackQueryHandler(callback=submit_hotel_food_callback,
                                                 pattern='food:submit',
                                                 pass_chat_data=True)


def adults_amount_callback(update: Update, context: CallbackContext) -> int:
    cid = update.effective_message.chat.id
    mid = context.bot.send_message(chat_id=cid,
                                   text=adults_text,
                                   reply_markup=adults_kb).message_id

    context.chat_data['message_with_kb'] = mid
    return ADULTS_FUNCTION


adults_amount_handler = CommandHandler(command='adults',
                                       callback=adults_amount_callback,
                                       pass_chat_data=True,
                                       )


def validate_adults_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    mid = context.chat_data['message_with_kb']
    q = update.callback_query.data.split(':')[-1]

    search_request = context.chat_data['search_request']
    pprint(search_request)
    search_request['adults'] = q

    context.bot.delete_message(chat_id=cid,
                               message_id=mid)
    context.bot.send_message(chat_id=cid,
                             text=f'Adults: {q}')

    return SEARCH_FUNCTIONS


validate_adults_handler = CallbackQueryHandler(callback=validate_adults_callback,
                                               pattern='adults:(.*)',
                                               pass_chat_data=True)


def kids_amount_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    mid = context.bot.send_message(chat_id=cid,
                                   text=kids_text,
                                   reply_markup=kids_kb).message_id

    context.chat_data['message_with_kb'] = mid
    return KIDS_FUNCTION


kids_amount_handler = CommandHandler(command='kids',
                                     callback=kids_amount_callback,
                                     pass_chat_data=True,
                                     )


def validate_kids_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    mid = context.chat_data['message_with_kb']
    q = update.callback_query.data.split(':')[-1]

    search_request = context.chat_data['search_request']
    pprint(search_request)
    search_request['kids'] = q

    context.bot.delete_message(chat_id=cid,
                               message_id=mid)
    context.bot.send_message(chat_id=cid,
                             text=f'Kids: {q}')
    return SEARCH_FUNCTIONS


validate_kids_handler = CallbackQueryHandler(callback=validate_kids_callback,
                                             pattern='kids:(.*)',
                                             pass_chat_data=True)


def nights_amount_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    update.message.reply_text(nights_amount_text)

    return NIGHTS_FUNCTION


nights_amount_handler = CommandHandler(command='nights',
                                       callback=nights_amount_callback,
                                       pass_chat_data=True,
                                       )


def validate_nights_callback(update: Update, context: CallbackContext) -> int:
    cid = update.effective_message.chat.id
    q = update.message.text
    try:
        q = int(q)
        if 0 > q or q > 21:
            raise ValueError
    except Exception as e:
        print(e)
        update.message.reply_text(wrong_input_text)
        return

    if q < 18:
        q = (q, q + 3)
    else:
        q = (q, q)

    search_request = context.chat_data['search_request']
    pprint(search_request)
    search_request['min_nights'], search_request['max_nights'] = q

    update.message.reply_text(f'Nights: {q[0]}-{q[1]}')
    return SEARCH_FUNCTIONS


validate_nights_handler = MessageHandler(callback=validate_nights_callback,
                                         pass_chat_data=True,
                                         filters=Filters.all)


def show_param_callback(update: Update, context: CallbackContext):
    search_request = context.chat_data['search_request']
    food = [food_list[i] for i in search_request['food']]
    stars = ['*' * (i + 1) for i in search_request['stars']]
    nights = f"{search_request['min_nights']}-{search_request['max_nights']}"
    stars = ', '.join(stars)
    food = ', '.join(food)

    update.message.reply_text(request_template_text.format(
        search_request['destination_country']+1,
        search_request['departure_city']+1,
        search_request['date'],
        stars,
        search_request['adults'],
        search_request['kids'],
        food,
        nights,
    ))


show_param_handler = CommandHandler(command='show',
                                    callback=show_param_callback,
                                    pass_chat_data=True,
                                    )

search_conversation_handler = ConversationHandler(
    entry_points=[start_handler],
    fallbacks=[],

    states={

        SEARCH_FUNCTIONS: [
            destination_country_handler,
            departure_city_handler,
            date_handler,
            hotel_stars_handler,
            hotel_food_handler,
            adults_amount_handler,
            kids_amount_handler,
            nights_amount_handler,
            # help_handler,
            show_param_handler,
            result_conversation_handler,
        ],
        DESTINATION_FUNCTION: [
            validate_destination_handler,
        ],
        DEPARTURE_FUNCTION: [
            validate_departure_handler,
        ],
        DATE_FUNCTION: [
            validate_date_handler,
        ],
        STARS_FUNCTION: [
            add_hotel_stars_handler,
            submit_hotel_stars_handler
        ],
        FOOD_FUNCTION: [
            add_hotel_food_handler,
            submit_hotel_food_handler
        ],
        ADULTS_FUNCTION: [
            validate_adults_handler,
        ],
        KIDS_FUNCTION: [
            validate_kids_handler,
        ],
        NIGHTS_FUNCTION: [
            validate_nights_handler
        ]

    },
    name='search_screen',
    persistent=False,
    allow_reentry=True,
)
