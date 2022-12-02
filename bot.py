import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
from os import environ
import requests
import babel.numbers
import decimal

# Credentials
load_dotenv('.env')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help(update, context):
    context.bot.send_message(chat_id='-1001397017207', text="oi")


def dolar(update, context):
    r = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL')
    bid = r.json()['USDBRL']['bid']

    context.bot.send_message(chat_id='-1001397017207', text=babel.numbers.format_currency(
        decimal.Decimal(bid), "BRL", locale='pt_BR', decimal_quantization=False))


def yen(update, context):
    r = requests.get('https://economia.awesomeapi.com.br/last/USD-JPY')
    bid = r.json()['USDJPY']['bid']

    context.bot.send_message(chat_id='-1001397017207', text=babel.numbers.format_currency(
        decimal.Decimal(bid), "JPY", locale='ja_JP', decimal_quantization=False))


def euro(update, context):
    r = requests.get('https://economia.awesomeapi.com.br/last/EUR-BRL')
    bid = r.json()['EURBRL']['bid']

    context.bot.send_message(chat_id='-1001397017207', text=babel.numbers.format_currency(
        decimal.Decimal(bid), "BRL", locale='pt_BR', decimal_quantization=False))


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(environ.get('TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("dolar", dolar))
    dp.add_handler(CommandHandler("yen", yen))
    dp.add_handler(CommandHandler("euro", euro))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.all, dolar))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
