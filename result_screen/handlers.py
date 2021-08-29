import telegram.error
from telegram.ext import (MessageHandler, Filters, CallbackContext, CallbackQueryHandler,
                          ConversationHandler, )
from telegram import (Update, ParseMode)
from search_screen.texts import (welcome_text)
from result_screen.texts import (test, empty_wishlist_text, tour_representation_text,
                                 hotel_representation_text, wishlist_representation_text,
                                 add_item_text, enter_name_text, enter_phone_text, choose_messager_text,
                                 incorrect_name_text, invalid_phone_text, user_data_text, uncomplete_formular_text)
from backend.selenium_parser import get_info
from decouple import config
from pprint import pprint
from regex import match, sub
from keyboards import (hotels_list_kb, tours_list_kb, one_tour_kb, result_reply_kb,
                       search_reply_kb, result_reply_buttons, one_item_wishlist_kb, wishlist_kb,
                       messager_kb, search_reply_buttons, admin_undone_kb)
from phonenumbers import carrier
from phonenumbers import parse
from phonenumbers.phonenumberutil import number_type
from database.tools import store_user

HOTELS_LIST_FUNCTION, TOURS_LIST_FUNCTION, WISHLIST_FUNCTION, APPLICATION_FUNCTION = range(9, 13)


def submit_request_callback(update: Update, context: CallbackContext):
    search_request = context.chat_data['search_request']
    cid = update.effective_chat.id

    if not search_request['destination_country'] or not search_request['departure_city'] or not search_request['date']:
        context.bot.send_message(chat_id=cid,
                                 text=uncomplete_formular_text,
                                 parse_mode=ParseMode.HTML,
                                 )

    search_request['stars'] = [str(i + 1) for i in search_request['stars']]
    search_request['food'] = [str(i + 2) for i in search_request['food']]

    mid = update.message.reply_text(text='Processing...').message_id
    cid = update.effective_chat.id

    result = get_info(search_request)
    current_hotel = result[0]
    try:
        context.bot.delete_message(chat_id=cid,
                                   message_id=mid, )
    except Exception as e:
        print(e)

    context.bot.send_message(chat_id=cid,
                             text='Uploaded!',
                             parse_mode=ParseMode.HTML,
                             reply_markup=result_reply_kb,
                             )

    mid = context.bot.send_message(chat_id=cid,
                                   text=hotel_representation_text.format(current_hotel['hotel_name'],
                                                                         current_hotel['town'],
                                                                         current_hotel['stars'],
                                                                         current_hotel['start_price']),
                                   parse_mode=ParseMode.HTML,
                                   reply_markup=hotels_list_kb,
                                   ).message_id

    payload = {
        'current_index': 0,
        'message_id': mid,
        'number_of_hotels': len(result),
        'hotels_info': result,
    }
    context.chat_data['hotels'] = payload
    context.chat_data['temporary_ids'] += [mid]

    return HOTELS_LIST_FUNCTION


submit_request_handler = MessageHandler(callback=submit_request_callback,
                                        pass_chat_data=True,
                                        filters=Filters.regex('^{}$'.format(search_reply_buttons[1][0])))


def back_to_search_callback(update: Update, context: CallbackContext):
    tids = context.chat_data['temporary_ids']
    cid = update.effective_chat.id

    try:
        for tid in tids:
            context.bot.delete_message(chat_id=cid,
                                       message_id=tid, )
    except Exception as e:
        print(e)

    username = update.message.chat.username
    context.bot.send_message(chat_id=cid,
                             text=welcome_text.format(username),
                             reply_markup=search_reply_kb)

    context.chat_data['temporary_ids'] = []
    return ConversationHandler.END


back_to_search_handler = MessageHandler(callback=back_to_search_callback,
                                        pass_chat_data=True,
                                        filters=Filters.regex('^{}$'.format(result_reply_buttons[0][2])))


def back_to_hotels_callback(update: Update, context: CallbackContext):
    tids = context.chat_data['temporary_ids']
    cid = update.effective_chat.id
    hotels = context.chat_data['hotels']
    current_hotel = hotels['hotels_info'][hotels['current_index']]

    try:
        for tid in tids:
            context.bot.delete_message(chat_id=cid,
                                       message_id=tid, )
            context.chat_data['temporary_ids'].remove(tid)

    except Exception as e:
        print(e)

    mid = context.bot.send_message(chat_id=cid,
                                   text=hotel_representation_text.format(current_hotel['hotel_name'],
                                                                         current_hotel['town'],
                                                                         current_hotel['stars'],
                                                                         current_hotel['start_price']),
                                   parse_mode=ParseMode.HTML,
                                   reply_markup=hotels_list_kb,
                                   ).message_id

    context.chat_data['hotels']['message_id'] = mid
    context.chat_data['temporary_ids'] += [mid]
    return HOTELS_LIST_FUNCTION


back_to_hotels_handler = MessageHandler(callback=back_to_hotels_callback,
                                        pass_chat_data=True,
                                        filters=Filters.regex('^{}$'.format(result_reply_buttons[0][0])))


def prev_next_hotel_callback(update: Update, context: CallbackContext) -> int:
    cid = update.effective_chat.id
    update.callback_query.answer()
    try:
        q = int(update.callback_query.data)
    except Exception as e:
        print(e)
        return HOTELS_LIST_FUNCTION

    hotels = context.chat_data['hotels']
    mid = hotels['message_id']
    hotel_index = (hotels['current_index'] + q) % hotels['number_of_hotels']
    current_hotel = hotels['hotels_info'][hotel_index]

    if hotel_index == hotels['current_index']: return HOTELS_LIST_FUNCTION
    try:
        context.bot.edit_message_text(chat_id=cid,
                                      message_id=mid,
                                      text=hotel_representation_text.format(current_hotel['hotel_name'],
                                                                            current_hotel['town'],
                                                                            current_hotel['stars'],
                                                                            current_hotel['start_price']),
                                      parse_mode=ParseMode.HTML,
                                      reply_markup=hotels_list_kb,
                                      )
    except telegram.error.TelegramError as e:

        mid = context.bot.send_message(chat_id=cid,
                                       text=hotel_representation_text.format(current_hotel['hotel_name'],
                                                                             current_hotel['town'],
                                                                             current_hotel['stars'],
                                                                             current_hotel['start_price']),
                                       parse_mode=ParseMode.HTML,
                                       reply_markup=hotels_list_kb,
                                       ).message_id

    hotels['current_index'] = (hotels['current_index'] + q) % hotels['number_of_hotels']
    hotels['message_id'] = mid

    context.chat_data['hotels'] = hotels

    return HOTELS_LIST_FUNCTION


prev_next_hotel_handler = CallbackQueryHandler(callback=prev_next_hotel_callback,
                                               pattern=f'^(-1|1)$',
                                               pass_chat_data=True)


def show_tour_callback(update: Update, context: CallbackContext) -> int:
    update.callback_query.answer()
    cid = update.effective_chat.id
    hotels = context.chat_data['hotels']
    mid = hotels['message_id']
    hotel_index = hotels['current_index']
    current_hotel = hotels['hotels_info'][hotel_index]
    pprint(current_hotel)
    tours = current_hotel['tours']
    current_tour = tours[0]
    kb = tours_list_kb
    if len(tours) < 2:
        kb = one_tour_kb
    context.bot.edit_message_text(chat_id=cid,
                                  message_id=mid,
                                  text=hotel_representation_text.format(current_hotel['hotel_name'],
                                                                        current_hotel['town'],
                                                                        current_hotel['stars'],
                                                                        current_hotel['start_price']),
                                  parse_mode=ParseMode.HTML, )

    mid = context.bot.send_message(chat_id=cid,
                                   text=tour_representation_text.format(current_tour['arrival_date'],
                                                                        current_tour['nights'],
                                                                        current_tour['room'],
                                                                        current_tour['food'],
                                                                        current_tour['price'],
                                                                        ),
                                   parse_mode=ParseMode.HTML,
                                   reply_markup=kb,
                                   ).message_id

    payload = {
        'current_index': 0,
        'message_id': mid,
        'number_of_tours': len(tours),
        'tours_info': tours,
    }

    context.chat_data['tours'] = payload
    context.chat_data['temporary_ids'] += [mid]

    return TOURS_LIST_FUNCTION


show_tour_handler = CallbackQueryHandler(callback=show_tour_callback,
                                         pattern=f'^tours$',
                                         pass_chat_data=True)


def prev_next_tour_callback(update: Update, context: CallbackContext) -> int:
    update.callback_query.answer()
    cid = update.effective_chat.id
    try:
        q = int(update.callback_query.data)
    except Exception as e:
        print(e)
        return TOURS_LIST_FUNCTION

    tours = context.chat_data['tours']
    mid = tours['message_id']
    tour_index = (tours['current_index'] + q) % tours['number_of_tours']
    current_tour = tours['tours_info'][tour_index]

    if tour_index == tours['current_index']: return TOURS_LIST_FUNCTION
    try:
        context.bot.edit_message_text(chat_id=cid,
                                      message_id=mid,
                                      text=tour_representation_text.format(current_tour['arrival_date'],
                                                                           current_tour['nights'],
                                                                           current_tour['room'],
                                                                           current_tour['food'],
                                                                           current_tour['price'],
                                                                           ),
                                      parse_mode=ParseMode.HTML,
                                      reply_markup=tours_list_kb,
                                      )
    except telegram.error.TelegramError as e:
        context.chat_data['temporary_ids'].remove(mid)
        mid = context.bot.send_message(chat_id=cid,
                                       text=tour_representation_text.format(current_tour['arrival_date'],
                                                                            current_tour['nights'],
                                                                            current_tour['room'],
                                                                            current_tour['food'],
                                                                            current_tour['price'],
                                                                            ),
                                       parse_mode=ParseMode.HTML,
                                       reply_markup=tours_list_kb,
                                       ).message_id
        context.chat_data['temporary_ids'] += [mid]
        tours['message_id'] = mid

    tours['current_index'] = (tours['current_index'] + q) % tours['number_of_tours']

    context.chat_data['tours'] = tours

    return TOURS_LIST_FUNCTION


prev_next_tour_handler = CallbackQueryHandler(callback=prev_next_tour_callback,
                                              pattern=f'^(-1|1)$',
                                              pass_chat_data=True)


def back_to_hotel_callback(update: Update, context: CallbackContext) -> int:
    update.callback_query.answer()
    cid = update.effective_chat.id

    hotels = context.chat_data['hotels']
    mid_hotel = hotels['message_id']
    mid_tour = context.chat_data['tours']['message_id']
    current_hotel = hotels['hotels_info'][hotels['current_index']]
    tids = context.chat_data['temporary_ids']

    try:
        context.bot.delete_message(chat_id=cid,
                                   message_id=mid_tour)
        context.bot.delete_message(chat_id=cid,
                                   message_id=mid_hotel)
        tids.remove(mid_tour)
        tids.remove(mid_hotel)

    except telegram.error.TelegramError as e:
        print(e)

    mid = context.bot.send_message(chat_id=cid,
                                   text=hotel_representation_text.format(current_hotel['hotel_name'],
                                                                         current_hotel['town'],
                                                                         current_hotel['stars'],
                                                                         current_hotel['start_price']),
                                   parse_mode=ParseMode.HTML,
                                   reply_markup=hotels_list_kb,
                                   ).message_id
    tids.append(mid)
    hotels['message_id'] = mid

    context.chat_data['hotels'] = hotels
    context.chat_data['temporary_ids'] = tids

    return HOTELS_LIST_FUNCTION


back_to_hotel_handler = CallbackQueryHandler(callback=back_to_hotel_callback,
                                             pattern=f'^back$',
                                             pass_chat_data=True)


def add_tour_callback(update: Update, context: CallbackContext) -> int:
    tours = context.chat_data['tours']
    tour_index = tours['current_index']
    current_tour = tours['tours_info'][tour_index]
    hotels = context.chat_data['hotels']
    current_hotel = dict(hotels['hotels_info'][hotels['current_index']])
    current_hotel.pop('tours', None)
    current_tour.update(current_hotel)

    wishlist = context.chat_data['wishlist']['wishlist_info']
    if current_tour not in wishlist:
        wishlist.append(current_tour)
        update.callback_query.answer(text='tour added!')
    else:
        wishlist.remove(current_tour)
        update.callback_query.answer(text='tour removed!')

    pprint(wishlist)
    context.chat_data['wishlist']['wishlist_info'] = wishlist

    return TOURS_LIST_FUNCTION


add_tour_handler = CallbackQueryHandler(callback=add_tour_callback,
                                        pattern=f'add',
                                        pass_chat_data=True)


def to_wishlist_callback(update: Update, context: CallbackContext) -> int:
    cid = update.effective_chat.id
    tids = context.chat_data['temporary_ids']
    wishlist = context.chat_data['wishlist']['wishlist_info']

    try:
        for tid in tids:
            context.bot.delete_message(chat_id=cid,
                                       message_id=tid)
    except telegram.error.TelegramError as e:
        print(e)

    kb = wishlist_kb if len(wishlist) > 1 else one_item_wishlist_kb

    if len(wishlist) < 1:
        mid = context.bot.send_message(chat_id=cid,
                                       text=empty_wishlist_text).message_id
        context.chat_data['temporary_ids'] = [mid]
        return WISHLIST_FUNCTION

    wishlist_item = wishlist[0]
    mid = context.bot.send_message(chat_id=cid,
                                   text=wishlist_representation_text.format(wishlist_item['hotel_name'],
                                                                            wishlist_item['town'],
                                                                            wishlist_item['arrival_date'],
                                                                            wishlist_item['nights'],
                                                                            wishlist_item['stars'],
                                                                            wishlist_item['room'],
                                                                            wishlist_item['food'],
                                                                            wishlist_item['price'], ),
                                   reply_markup=kb).message_id

    context.chat_data['temporary_ids'] = [mid]
    payload = {'message_id': mid,
               'current_index': 0,
               'number_of_items': len(wishlist),
               'wishlist_info': wishlist}
    context.chat_data['wishlist'] = payload

    return WISHLIST_FUNCTION


to_wishlist_handler = MessageHandler(callback=to_wishlist_callback,
                                     pass_chat_data=True,
                                     filters=Filters.regex(r'^{}$'.format(result_reply_buttons[0][1])))


def prev_next_wishlist_callback(update: Update, context: CallbackContext) -> int:
    update.callback_query.answer()
    cid = update.effective_chat.id
    try:
        q = int(update.callback_query.data)
    except Exception as e:
        print(e)
        return TOURS_LIST_FUNCTION

    wishlist = context.chat_data['wishlist']
    mid = wishlist['message_id']
    wishlist_index = (wishlist['current_index'] + q) % wishlist['number_of_items']
    wishlist_item = wishlist['wishlist_info'][wishlist_index]

    try:
        context.bot.edit_message_text(chat_id=cid,
                                      message_id=mid,
                                      text=wishlist_representation_text.format(wishlist_item['hotel_name'],
                                                                               wishlist_item['town'],
                                                                               wishlist_item['arrival_date'],
                                                                               wishlist_item['nights'],
                                                                               wishlist_item['stars'],
                                                                               wishlist_item['room'],
                                                                               wishlist_item['food'],
                                                                               wishlist_item['price'], ),
                                      reply_markup=wishlist_kb)
    except telegram.error.TelegramError as e:
        print(e)
        context.chat_data['temporary_ids'].remove(mid)
        mid = context.bot.send_message(chat_id=cid,
                                       text=wishlist_representation_text.format(wishlist_item['hotel_name'],
                                                                                wishlist_item['town'],
                                                                                wishlist_item['arrival_date'],
                                                                                wishlist_item['nights'],
                                                                                wishlist_item['stars'],
                                                                                wishlist_item['room'],
                                                                                wishlist_item['food'],
                                                                                wishlist_item['price'], ),
                                       reply_markup=wishlist_kb).message_id
        wishlist['message_id'] = mid

        context.chat_data['temporary_ids'] += [mid]

    wishlist['current_index'] = (wishlist['current_index'] + q) % wishlist['number_of_items']

    context.chat_data['wishlist'] = wishlist

    return WISHLIST_FUNCTION


prev_next_wishlist_handler = CallbackQueryHandler(callback=prev_next_wishlist_callback,
                                                  pattern=f'^(-1|1)$',
                                                  pass_chat_data=True)


def del_from_wishlist_callback(update: Update, context: CallbackContext) -> int:
    update.callback_query.answer()
    cid = update.effective_chat.id

    wishlist = context.chat_data['wishlist']
    mid = wishlist['message_id']
    wishlist['wishlist_info'].pop(wishlist['current_index'])
    kb = wishlist_kb if len(wishlist['wishlist_info']) > 1 else one_item_wishlist_kb

    if len(wishlist['wishlist_info']) == 0:
        wishlist['number_of_items'] = 0
        wishlist['current_index'] = -1
        try:
            context.bot.edit_message_text(chat_id=cid,
                                          message_id=mid,
                                          text=empty_wishlist_text, )
        except telegram.error.TelegramError as e:
            print(e)
            context.chat_data['temporary_ids'].remove(mid)
            mid = context.bot.send_message(chat_id=cid,
                                           text=empty_wishlist_text,
                                           ).message_id
            context.chat_data['temporary_ids'] += [mid]
            wishlist['message_id'] = mid

    else:
        wishlist['number_of_items'] -= 1
        wishlist['current_index'] = (wishlist['current_index'] + 1) % wishlist['number_of_items']
        wishlist_item = wishlist['wishlist_info'][wishlist['current_index']]
        try:
            context.bot.edit_message_text(chat_id=cid,
                                          message_id=mid,
                                          text=wishlist_representation_text.format(wishlist_item['hotel_name'],
                                                                                   wishlist_item['town'],
                                                                                   wishlist_item['arrival_date'],
                                                                                   wishlist_item['nights'],
                                                                                   wishlist_item['stars'],
                                                                                   wishlist_item['room'],
                                                                                   wishlist_item['food'],
                                                                                   wishlist_item['price'], ),
                                          reply_markup=kb)
        except telegram.error.TelegramError as e:
            print(e)
            context.chat_data['temporary_ids'].remove(mid)
            mid = context.bot.send_message(chat_id=cid,
                                           text=wishlist_representation_text.format(wishlist_item['hotel_name'],
                                                                                    wishlist_item['town'],
                                                                                    wishlist_item['arrival_date'],
                                                                                    wishlist_item['nights'],
                                                                                    wishlist_item['stars'],
                                                                                    wishlist_item['room'],
                                                                                    wishlist_item['food'],
                                                                                    wishlist_item['price'], ),
                                           reply_markup=kb).message_id
            context.chat_data['temporary_ids'] += [mid]
            wishlist['message_id'] = mid

    context.chat_data['wishlist'] = wishlist

    return WISHLIST_FUNCTION


del_from_wishlist_handler = CallbackQueryHandler(callback=del_from_wishlist_callback,
                                                 pattern=f'^remove$',
                                                 pass_chat_data=True)


def send_application_callback(update: Update, context: CallbackContext) -> int:
    cid = update.effective_chat.id
    tids = context.chat_data['temporary_ids']
    wishlist = context.chat_data['wishlist']['wishlist_info']

    try:
        for tid in tids:
            context.bot.delete_message(chat_id=cid,
                                       message_id=tid)
    except telegram.error.TelegramError as e:
        print(e)

    kb = wishlist_kb if len(wishlist) > 1 else one_item_wishlist_kb

    if len(wishlist) < 1:
        mid = context.bot.send_message(chat_id=cid,
                                       text=add_item_text).message_id
        context.chat_data['temporary_ids'] = [mid]
        return WISHLIST_FUNCTION

    mid = context.bot.send_message(chat_id=cid,
                                   text=enter_name_text).message_id

    context.chat_data['temporary_ids'] = [mid]

    return APPLICATION_FUNCTION


send_application_handler = MessageHandler(callback=send_application_callback,
                                          pass_chat_data=True,
                                          filters=Filters.regex('^{}$'.format(result_reply_buttons[1][0])))


def validate_name_callback(update: Update, context: CallbackContext) -> int:
    cid = update.effective_chat.id
    q = update.message.text

    application = context.chat_data['application']

    if application['name']:
        return APPLICATION_FUNCTION

    if not match('^\p{L}*\s\p{L}*$', q):
        mid = context.bot.send_message(chat_id=cid,
                                       text=incorrect_name_text).message_id
        context.chat_data['temporary_ids'] += [mid]

        return APPLICATION_FUNCTION
    name = []
    for el in q.split(' '):
        if match(r'\s', el):
            continue
        el = list(el)
        el[0] = el[0].upper()
        name += [''.join(el)]

    application['name'] = ' '.join(name)
    context.chat_data['application'] = application

    mid = context.bot.send_message(chat_id=cid,
                                   text=enter_phone_text).message_id

    context.chat_data['temporary_ids'] += [mid]

    return APPLICATION_FUNCTION


validate_name_handler = MessageHandler(callback=validate_name_callback,
                                       pass_chat_data=True,
                                       filters=Filters.regex(r'(?:(?![0-9_])[\w])+'))


def validate_phone_callback(update: Update, context: CallbackContext) -> int:
    cid = update.effective_chat.id
    q = update.message.text

    application = context.chat_data['application']

    if not application['name'] or application['phone']:
        return APPLICATION_FUNCTION

    try:
        phone = sub(r'\s+', '', q)
        if not carrier._is_mobile(number_type(parse(phone))):
            raise ValueError
    except Exception as e:
        print(e)
        mid = context.bot.send_message(chat_id=cid,
                                       text=invalid_phone_text).message_id
        context.chat_data['temporary_ids'] += [mid]
        return APPLICATION_FUNCTION

    application['phone'] = phone
    context.chat_data['application'] = application

    mid = context.bot.send_message(chat_id=cid,
                                   text=choose_messager_text,
                                   reply_markup=messager_kb).message_id

    context.chat_data['temporary_ids'] += [mid]


validate_phone_handler = MessageHandler(callback=validate_phone_callback,
                                        pass_chat_data=True,
                                        filters=Filters.regex(r'\d+|\+'))


def validate_messager_callback(update: Update, context: CallbackContext) -> int:
    cid = update.effective_chat.id
    q = update.callback_query.data.split(':')[1]
    wishlist = context.chat_data['wishlist']['wishlist_info']
    application = context.chat_data['application']
    application['messager'] = q
    context.chat_data['application'] = application
    admin_id = int(config('TEST_ADMIN_ID'))

    tids = context.chat_data['temporary_ids']

    try:
        for tid in tids:
            context.bot.delete_message(chat_id=cid,
                                       message_id=tid, )
            context.chat_data['temporary_ids'].remove(tid)

    except Exception as e:
        print(e)

    context.bot.send_message(chat_id=cid,
                             text=user_data_text.format(application['name'],
                                                        application['phone'],
                                                        application['messager']))
    context.bot.send_message(chat_id=admin_id,
                             text=user_data_text.format(application['name'],
                                                        application['phone'],
                                                        application['messager']),
                             reply_markup=admin_undone_kb)

    for wishlist_item in wishlist:
        for cid in [admin_id, cid]:
            context.bot.send_message(chat_id=cid,
                                     text=wishlist_representation_text.format(wishlist_item['hotel_name'],
                                                                              wishlist_item['town'],
                                                                              wishlist_item['arrival_date'],
                                                                              wishlist_item['nights'],
                                                                              wishlist_item['stars'],
                                                                              wishlist_item['room'],
                                                                              wishlist_item['food'],
                                                                              wishlist_item['price']))
    user_info = {
        'uid': update.effective_message.from_user.id,
        'name': application['name'],
        'phone': application['phone'],
        'messager': application['messager'],
        'username': update.effective_message.from_user.first_name,
        'wishlist': wishlist,
    }

    store_user(user_info)

    payload = {'message_id': 0,
               'current_index': 0,
               'number_of_items': 0,
               'wishlist_info': []}
    context.chat_data['wishlist'] = payload
    context.chat_data['application'] = {'name': '',
                                        'phone': '',
                                        'messager': ''}

    return APPLICATION_FUNCTION


validate_messager_handler = CallbackQueryHandler(callback=validate_messager_callback,
                                                 pattern=r"messager:(.*)",
                                                 pass_chat_data=True)

result_conversation_handler = ConversationHandler(
    entry_points=[submit_request_handler],
    states={
        HOTELS_LIST_FUNCTION: [
            prev_next_hotel_handler,
            show_tour_handler,
            back_to_hotels_handler,
            to_wishlist_handler,
            send_application_handler,

        ],
        TOURS_LIST_FUNCTION: [
            back_to_hotel_handler,
            prev_next_tour_handler,
            add_tour_handler,
            back_to_hotels_handler,
            to_wishlist_handler,
            send_application_handler,
        ],
        WISHLIST_FUNCTION: [
            prev_next_wishlist_handler,
            del_from_wishlist_handler,
            back_to_hotels_handler,
            to_wishlist_handler,
            send_application_handler,
        ],
        APPLICATION_FUNCTION: [
            validate_name_handler,
            validate_phone_handler,
            validate_messager_handler,
            back_to_hotels_handler,
            to_wishlist_handler,
        ],

    },
    fallbacks=[back_to_search_handler],
    name='result_screen',
    persistent=False,
)
