#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

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

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Hola! soc el bot del IES RL \U0001F3EB. Pots demanar el que vulguis. '
        'Què vols saber:\n\n'
        'Quins /estudis s\'imparteixen al centre?\n'
        'Quin és el /telefon del centre\n'
        'On ens /trobam?\n'
    )



def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Para ver la carta utiliza el comando /carta')

def telefon(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('El nostre telèfon és el 971 76 31 00')

def trobam(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Ens trobaràs a Av. de Portugal, 2, 07012 Palma, Illes Balears')

def estudis(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'El centre ofereix estudis d\'/ESO, /batxillerat i /cicles formatius '        
    )

def cicles(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Al centre es poden cursar els següents /estudis de cicles formatius\n\n '
        '\u2705  /FPBasica d\'informàtica d\'oficina\n'
        '\u2705  Grau mitjà d\'atenció a persones en situació de dependència\n'
        '\u2705  Grau superior d\' ́integració social\n'
        '\u2705  Grau superior d\'animació sociocultural i turística\n'
        '\n\nTorna al principi amb /start\n\n'
    )

def batxillerat(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Sobre quina modalitat vols informació?\n\n '
        '\u2705 Modalitat de ciències /batxCIEN\n '
        '\u2705 Modalitat d\'humanitats /batxHUMAN\n '
        '\u2705 Modalitat de ciències socials /batxCCSS\n '    
        '\n\nTorna al principi amb /start\n\n'
    )
    

def batxCIEN(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Matèries troncals\n\n '
        '\U0001F4D7 Filosofia (3)\n '
        '\U0001F4D7 Llengua catalana i literatura (2,5)\n '
        '\U0001F4D7 Llengua castellana i literatura I (2,5)\n '
        '\U0001F4D7 Matemàtiques I (4)\n '
        '\U0001F4D7 Primera llengua estrangera I (3)\n\n '
        'Se n’han de triar 2 entre:\n\n '
        '\U0001F4D7 Biologia i geologia (4)\n '
        '\U0001F4D7 Dibuix tècnic I (4)\n '
        '\U0001F4D7 Física i química (4)\n\n '
        'Matèries específiques. Se n’han de triar 2 entre:\n\n '
        '\U0001F4D8 Tecnologia industrial I /ti1 (3)\n '
        '\U0001F4D8 Tecnologies de la informació i la comunicació I (3)\n '
        '\U0001F4D8 Cultura científica (3)\n '
        '\U0001F4D8 Segona llengua estrangera I (3)\n '
        '\U0001F4D8 Anatomia aplicada (3)\n '
        '\U0001F4D8 Religió(3)\n '
    )    




def fpbasica(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Aquests estudis de /cicles formatius es fan en horari d\'horabaixa\n\n '
        '1r curs\n\n'
        '\U0001F4D7 Ofimàtica i arxiu de documents 8\n '
        '\U0001F4D7 Muntatge i manteniment de sistemes i components informàtics 10\n '
        '\U0001F4D7 Ciències aplicades I 5\n '
        '\U0001F4D7 Comunicació i societat I 5\n '
        '\U0001F4D7 Tutoria 2\n\n'
        'Total hores setmanals 30\n\n'

        '2n curs\n\n'
        '\U0001F4D8 Operacions per la configuració i exportació 8\n '
        '\U0001F4D8 Instalació i mantenimet de xarxes 7\n '
        '\U0001F4D8 Ciències aplicades II 6\n '
        '\U0001F4D8 Comunicació i societat II 7\n '
        '\U0001F4D8 Tutoria 2\n\n '
        'Total hores setmanals 30\n '
        '\n\nTorna al principi amb /start\n\n'

    )

def ti1(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Temari de Tecnologia industrial I\n\n '
        'Circuits i sistemes lògics\n'
        'Control i programació de sistemes automàtics\n'
        'Sistemes automàtics\n'
        'Principis de màquines\n'
        'Materials\n'
        'Aplicacions amb robòtica i arduino\n'
    )

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)




def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1471785144:AAHrsIs6sGPLoGJtilaT7oYlquLyG6jda3o", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("telefon", telefon))
    dispatcher.add_handler(CommandHandler("trobam", trobam))
    dispatcher.add_handler(CommandHandler("estudis", estudis))
    dispatcher.add_handler(CommandHandler("cicles", cicles))
    dispatcher.add_handler(CommandHandler("FPBasica", fpbasica))
    dispatcher.add_handler(CommandHandler("batxillerat", batxillerat))
    dispatcher.add_handler(CommandHandler("batxCIEN", batxCIEN))
    dispatcher.add_handler(CommandHandler("ti1", ti1))
    
    
    


    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()