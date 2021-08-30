import telegram.error
from telegram.ext import (Filters, CallbackContext, CallbackQueryHandler,
                          ConversationHandler, CommandHandler, )
from telegram import (Update, ParseMode)

from admin_screen.texts import welcome_admin_text, desc_admin_text
from pprint import pprint
from keyboards import (admin_done_kb, admin_undone_kb)
from decouple import config

MAIN_FUNCTION = range(13, 14)


def start_admin_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    username = update.message.chat.username
    context.bot.send_message(chat_id=cid,
                             text=welcome_admin_text,
                             )
    context.bot.send_message(chat_id=cid,
                             text=desc_admin_text,
                             )

    return MAIN_FUNCTION


start_admin_handler = CommandHandler(command='start',
                                     callback=start_admin_callback,
                                     pass_chat_data=True,
                                     filters=Filters.chat(int(config('TEST_ADMIN_ID'))))


# def mark_offer_callback(update: Update, context: CallbackContext):
#     cid = update.effective_message.chat.id
#     mid = update.effective_message.message_id
#     q = update.callback_query.data
#     update.callback_query.answer()
#
#     if q == 'done':
#         kb = admin_undone_kb
#     else:
#         kb = admin_done_kb
#
#     context.bot.edit_message_reply_markup(chat_id=cid,
#                                           message_id=mid,
#                                           reply_markup=kb)

#
# mark_offer_handler = CallbackQueryHandler(callback=mark_offer_callback,
#                                           pass_chat_data=True,
#                                           pattern=r'admin:(.*)',
#                                           )

# admin_conversation_handler = ConversationHandler(
#     entry_points=[start_admin_handler],
#     fallbacks=[],
#
#     states={
#         MAIN_FUNCTION: [
#             # mark_offer_handler
#         ],
#     },
#     name='admin_screen',
#     persistent=False,
#     allow_reentry=True,
# )
