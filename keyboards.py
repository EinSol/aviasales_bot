from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton)

food_list = ['RO', 'BB', 'HB', 'FB', 'AI', 'UAI']
messager_list = ['Telegram', 'Viber', "What'sUp"]
adults_buttons = [InlineKeyboardButton(text=f'{i}',
                                       callback_data=f'adults:{i}') for i in range(1, 7)]
kids_buttons = [InlineKeyboardButton(text=f'{i}',
                                     callback_data=f'kids:{i}') for i in range(4)]
stars_buttons = [InlineKeyboardButton(text=f'{i + 1}',
                                      callback_data=f'stars:{i}') for i in range(5)]
stars_buttons += [InlineKeyboardButton(text=f'отправить', callback_data=f'stars:submit')]

food_buttons = [InlineKeyboardButton(text=f'{type_food}',
                                     callback_data=f'food:{i}') for type_food, i in zip(food_list, range(6))]
food_buttons += [InlineKeyboardButton(text=f'отправить', callback_data=f'food:submit')]
messager_buttons = [InlineKeyboardButton(text=f'{item}',
                                         callback_data=f'messager:{item}') for item in messager_list]

prev_button = InlineKeyboardButton(text=f'предыдуший', callback_data=f'-1')
next_button = InlineKeyboardButton(text=f'следующий', callback_data=f'1')
del_item_button = InlineKeyboardButton(text=f'удалить', callback_data=f'remove')
to_tours_button = InlineKeyboardButton(text=f'показать туры', callback_data=f'tours')
add_tour_button = InlineKeyboardButton(text=f'добавить в список', callback_data=f'add')
back_tour_button = InlineKeyboardButton(text=f'к отелям', callback_data=f'back')
# done_button = InlineKeyboardButton(text=f'done', callback_data=f'admin:done')
# undone_button = InlineKeyboardButton(text=f'undone', callback_data=f'admin:undone')
result_reply_buttons = [['к отелям', 'к списку', 'к поиску'], ['отправить заявку']]
search_reply_buttons = [['куда', 'откуда', 'когда'], ['поиск']]

milaTaras1
adults_kb = InlineKeyboardMarkup([adults_buttons[i:i + 2] for i in range(0, len(adults_buttons), 2)])
kids_kb = InlineKeyboardMarkup([kids_buttons[i:i + 2] for i in range(0, len(kids_buttons), 2)])
stars_kb = InlineKeyboardMarkup([stars_buttons[i:i + 2] for i in range(0, len(stars_buttons), 2)])
food_kb = InlineKeyboardMarkup([food_buttons[i:i + 2] for i in range(0, len(food_buttons), 2)])
hotels_list_kb = InlineKeyboardMarkup([[prev_button, next_button], [to_tours_button]])
tours_list_kb = InlineKeyboardMarkup([[prev_button, next_button], [back_tour_button, add_tour_button]])
one_tour_kb = InlineKeyboardMarkup([[back_tour_button, add_tour_button]])
wishlist_kb = InlineKeyboardMarkup([[prev_button, next_button], [del_item_button]])
one_item_wishlist_kb = InlineKeyboardMarkup([[del_item_button]])
messager_kb = InlineKeyboardMarkup([messager_buttons])

# admin_done_kb=InlineKeyboardMarkup([[done_button]])
# admin_undone_kb=InlineKeyboardMarkup([[undone_button]])

result_reply_kb = ReplyKeyboardMarkup(keyboard=result_reply_buttons,
                                      resize_keyboard=True, )
search_reply_kb = ReplyKeyboardMarkup(keyboard=search_reply_buttons,
                                      resize_keyboard=True, )
