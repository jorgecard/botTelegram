#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.
# prueba de edición

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import codecs

import iptv_cuentas as iptv

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
# from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

tornar = '\n\nVuelve al principio con /start\n\n'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    name = update.message.from_user.username
    update.message.reply_text(
        f"Hola {name}, soy el *bot de NanoTech * \U0001F3EB. Puedes pedir lo que desees. ", parse_mode='Markdown'
    )
    update.message.reply_text(
        'Qué deseas saber:\n\n'
        '1. Clientes por /vencer\n'
        '2. Clientes /activos\n'
        '3. Clientes /inactivos\n'
        '4. /location\n'
        '5. /tic\n'
        '![Foto de l\'institut\'](https://www.casaljoanalcover.es/wp-content/uploads/2014/03/1195690728_f.jpg)', parse_mode='Markdown'
    )
    update.message.reply_text(tornar)

def por_vencer(update: Update, context: CallbackContext) -> None:
    mensaje_con_clientes = iptv.por_vencer()
    update.message.reply_text(mensaje_con_clientes)
    update.message.reply_text(tornar)

def vencidos(update: Update, context: CallbackContext) -> None:
    mensaje_con_clientes = iptv.vencidos()
    update.message.reply_text(mensaje_con_clientes)
    update.message.reply_text(tornar)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def location(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        'Cerca del monay shopping \n\n'
        '![Como llegar](https://goo.gl/maps/Qumc4t8dA9fMCPu79)', parse_mode='Markdown'
    )


def tic(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    # update.message.reply_text('https://youtu.be/LXdOqeuG438')
    f = codecs.open('botTelegram/info/tic.md', encoding='utf-8')
    update.message.reply_text(f.read(), parse_mode='Markdown')


def programacion(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        '```python\n'
        's = "Python syntax highlighting"\n'
        'print s\n'
        '```\n', parse_mode='Markdown'
    )

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("5049299291:AAGimNKtuj3SCuGAVv8ARNpApH5Vsop4iA4", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("vencer", por_vencer))
    dispatcher.add_handler(CommandHandler("inactivos", vencidos))

    dispatcher.add_handler(CommandHandler("location", location))
    dispatcher.add_handler(CommandHandler("tic", tic))
    dispatcher.add_handler(CommandHandler("programacion", programacion))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
#         filters.TEXT & filters.Entity(echo)))
        Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
