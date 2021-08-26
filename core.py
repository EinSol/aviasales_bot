
from telegram.ext import Updater, CommandHandler
from decouple import config
import sentry_sdk
import logging
from logdna import LogDNAHandler
from sentry_sdk.integrations.logging import LoggingIntegration
from search_screen.handlers import search_conversation_handler
from admin_screen.handlers import admin_conversation_handler


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(message)s')

logDNAoptions = dict()
logDNAoptions['index_meta'] = True
# logDNAoptions['hostname'] = config('HOSTNAME', default='localhost')
logDNAhandler = LogDNAHandler(config('LOGDNA_KEY'), options=logDNAoptions)

logger = logging.getLogger()
logger.addHandler(logDNAhandler)

sentry_logging = LoggingIntegration(
    level=logging.DEBUG,
    event_level=logging.ERROR
)

sentry_sdk.init(
    config('SENTRY_URL'),
    traces_sample_rate=1.0,
    integrations=[sentry_logging]
)


class AviasalesBot:
    def __init__(self, token: str):
        self.__api_token = token
        self.updater = Updater(token=self.__api_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.job_q = self.updater.job_queue


if __name__ == '__main__':
    env = config('ENV', default='DEBUG')

    if env == 'DEBUG':
        bot = AviasalesBot(config('BOT_TEST_TOKEN'))
    elif env == 'PRODUCTION':
        bot = AviasalesBot(config('BOT_TOKEN'))
    else:
        raise EnvironmentError

    bot.dispatcher.add_handler(CommandHandler("debug", lambda u, _: u.message.reply_text("I'm up!")), group=-666)
    bot.dispatcher.add_handler(admin_conversation_handler)
    bot.dispatcher.add_handler(search_conversation_handler)
    bot.updater.start_polling()
    bot.updater.idle()

