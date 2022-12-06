import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
from os import environ
import requests
from babel.numbers import format_currency
from decimal import Decimal, InvalidOperation

# Credentials
load_dotenv('.env')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# chat_id = update.message.chat.id

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text("Hi, I'm DolarBot.")


def help(update, context):
    update.message.reply_text('''
Hello there! My name is DolarBot.
*Main* commands available:
    /dolar (optional value): Converts USD to BRL.
    /euro (optional value): Converts EUR to BRL.
    /yen (optional value): Converts JPY to BRL.
    /btc (optional value): Converts BTC to BRL.
    /doge (optional value): Converts DOGE to BRL.
    /eth (optional value): Converts ETH to BRL.
''', parse_mode='MARKDOWN')


def dolar(update, context):
    try:
        r = requests.get('https://economia.awesomeapi.com.br/json/last/USD-BRL')
        bid = r.json()['USDBRL']['bid']

        dolar = Decimal(context.args[0]) * Decimal(bid)

        update.message.reply_text(format_currency(dolar, "BRL", locale='pt_BR', decimal_quantization=False))
    except IndexError as e:
        # Argument was not passed
        update.message.reply_text(format_currency(Decimal(bid), "BRL", locale='pt_BR', decimal_quantization=False))
    except InvalidOperation as e:
        update.message.reply_text("Valor inválido!")


def euro(update, context):
    try:
        r = requests.get('https://economia.awesomeapi.com.br/json/last/EUR-BRL')
        bid = r.json()['EURBRL']['bid']

        euro = Decimal(context.args[0]) * Decimal(bid)

        update.message.reply_text(format_currency(euro, "BRL", locale='pt_BR', decimal_quantization=False))
    except IndexError as e:
        # Argument was not passed
        update.message.reply_text(format_currency(Decimal(bid), "BRL", locale='pt_BR', decimal_quantization=False))
    except InvalidOperation as e:
        update.message.reply_text("Valor inválido!")


def yen(update, context):
    try:
        r = requests.get('https://economia.awesomeapi.com.br/json/last/JPY-BRL')
        bid = r.json()['JPYBRL']['bid']

        yen = Decimal(context.args[0]) * Decimal(bid)

        update.message.reply_text(format_currency(yen, "BRL", locale='pt_BR', decimal_quantization=False))
    except IndexError as e:
        # Argument was not passed
        update.message.reply_text(format_currency(Decimal(bid), "BRL", locale='pt_BR', decimal_quantization=False))
    except InvalidOperation as e:
        update.message.reply_text("Valor inválido!")


def btc(update, context):
    try:
        # r = requests.get('https://economia.awesomeapi.com.br/json/last/BTC-BRL')
        # bid = r.json()['BTCBRL']['bid']
        r = requests.get('https://www.mercadobitcoin.net/api/BTC/ticker/')
        bid = r.json()['ticker']['last']

        btc = Decimal(context.args[0]) * Decimal(bid)

        update.message.reply_text(format_currency(btc, "BRL", locale='pt_BR', decimal_quantization=False))
    except IndexError as e:
        # Argument was not passed
        update.message.reply_text(format_currency(Decimal(bid), "BRL", locale='pt_BR', decimal_quantization=False))
    except InvalidOperation as e:
        update.message.reply_text("Valor inválido!")


def doge(update, context):
    try:
        # r = requests.get('https://economia.awesomeapi.com.br/json/last/DOGE-BRL')
        # bid = r.json()['DOGEBRL']['bid']
        r = requests.get('https://www.mercadobitcoin.net/api/DOGE/ticker/')
        bid = r.json()['ticker']['last']

        doge = Decimal(context.args[0]) * Decimal(bid)

        update.message.reply_text(format_currency(doge, "BRL", locale='pt_BR', decimal_quantization=False))
    except IndexError as e:
        # Argument was not passed
        update.message.reply_text(format_currency(Decimal(bid), "BRL", locale='pt_BR', decimal_quantization=False))
    except InvalidOperation as e:
        update.message.reply_text("Valor inválido!")


def eth(update, context):
    try:
        # r = requests.get('https://economia.awesomeapi.com.br/json/last/ETH-BRL')
        # bid = r.json()['ETHBRL']['bid']
        r = requests.get('https://www.mercadobitcoin.net/api/ETH/ticker/')
        bid = r.json()['ticker']['last']

        eth = Decimal(context.args[0]) * Decimal(bid)

        update.message.reply_text(format_currency(eth, "BRL", locale='pt_BR', decimal_quantization=False))
    except IndexError as e:
        # Argument was not passed
        update.message.reply_text(format_currency(Decimal(bid), "BRL", locale='pt_BR', decimal_quantization=False))
    except InvalidOperation as e:
        update.message.reply_text("Valor inválido!")


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
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("dolar", dolar))
    dp.add_handler(CommandHandler("euro", euro))
    dp.add_handler(CommandHandler("yen", yen))
    dp.add_handler(CommandHandler("btc", btc))
    dp.add_handler(CommandHandler("doge", doge))
    dp.add_handler(CommandHandler("eth", eth))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.all, start))

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
