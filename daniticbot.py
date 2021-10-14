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
import codecs

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

tornar = '\n\nTorna al principi amb /start\n\n'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    name = update.message.from_user.username
    update.message.reply_text(
        f"Hola {name}, soc el *bot de TIC de l\'IES RL* \U0001F3EB. Pots demanar el que vulguis. ", parse_mode='Markdown'
    )
    update.message.reply_text(
        'Què vols saber:\n\n'
        '1. Quins /estudis s\'imparteixen al centre?\n'
        '2. Quines matèries o estudis de /tic puc fer a l\'institut?\n'
        '3. Quin és el /telefon del centre o /correuelectronic per a contactar\n'
        '4. On ens /trobam?\n'
        '5. /blogs dels alumnes AICLE\n\n'
        '6. Conèixer els diferents /espais del centre\n\n'
        '![Foto de l\'institut\'](https://www.casaljoanalcover.es/wp-content/uploads/2014/03/1195690728_f.jpg)', parse_mode='Markdown'
    )
    update.message.reply_text(tornar)


def correuelectronic(update: Update, context: CallbackContext) -> None:

    update.message.reply_text(
        'iesramonllull@educaib.eu'
    )
    update.message.reply_text(tornar)


def peli(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Mi chiste'
    )


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def telegram(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Telegram es una aplicación de mensajería instantánea de código abierto, segura, privada, multi-plataforma, rápida, basada en la nube y gratuita'
    )


def telefon(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('El nostre telèfon és el 971 76 31 00')


def trobam(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        'Ens trobaràs a Av. de Portugal, 2, 07012 Palma, Illes Balears \n\n'
        '![Com arribar](https://www.google.com/maps/dir//IES+Ramon+Llull,+Av.+de+Portugal,+2,+07012+Palma,+Illes+Balears/@39.576389,2.6449765,17.75z/data=!4m16!1m6!3m5!1s0x1297925975bb3921:0x567142aba6eb836!2sIES+Ramon+Llull!8m2!3d39.5764471!4d2.6453479!4m8!1m0!1m5!1m1!1s0x1297925975bb3921:0x567142aba6eb836!2m2!1d2.6453479!2d39.5764471!3e2)', parse_mode='Markdown'
    )


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


def tic(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    # update.message.reply_text('https://youtu.be/LXdOqeuG438')
    f = codecs.open('botTelegram/info/tic.md', encoding='utf-8')
    update.message.reply_text(f.read(), parse_mode='Markdown')


def espais(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    # update.message.reply_text('https://youtu.be/LXdOqeuG438')
    f = codecs.open('botTelegram/info/espais.md', encoding='utf-8')
    update.message.reply_text(f.read(), parse_mode='Markdown')


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
        'Són cicles formatius d\'una durada de **2 anys acadèmics** destinats a persones que no han finalitzat l\'ESO i vol prosseguir els seus estudis cap a a un camp de la Formació Professional.\n\n '
        'Aquests estudis de /cicles formatius es fan en *horari d\'horabaixa*\n\n '
        '*1r curs*\n\n'
        '\U0001F4D7 Ofimàtica i arxiu de documents 8\n '
        '\U0001F4D7 Muntatge i manteniment de sistemes i components informàtics 10\n '
        '\U0001F4D7 Ciències aplicades I 5\n '
        '\U0001F4D7 Comunicació i societat I 5\n '
        '\U0001F4D7 Tutoria 2\n\n'
        'Total hores setmanals 30\n\n'

        '*2n curs*\n\n'
        '\U0001F4D8 Operacions per la configuració i exportació 8\n '
        '\U0001F4D8 Instalació i mantenimet de xarxes 7\n '
        '\U0001F4D8 Ciències aplicades II 6\n '
        '\U0001F4D8 Comunicació i societat II 7\n '
        '\U0001F4D8 Tutoria 2\n\n '
        'Total hores setmanals 30\n '
        '\n\nTorna al principi amb /start\n\n', parse_mode='Markdown'
    )


def ti1(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Temari de Tecnologia industrial I\n\n '
        '\U0001F4D8 Circuits i sistemes lògics\n'
        '\U0001F4D8 Control i programació de sistemes automàtics\n'
        '\U0001F4D8 Sistemes automàtics\n'
        '\U0001F4D8 Principis de màquines\n'
        '\U0001F4D8 Materials\n'
        '\U0001F4D8 Aplicacions amb robòtica i arduino\n'
    )


def tic4eso(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    # update.message.reply_text('https://youtu.be/LXdOqeuG438')
    f = codecs.open('info/tic4eso.md', encoding='utf-8')
    update.message.reply_text(f.read(), parse_mode='Markdown')


def programacion(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        '```python\n'
        's = "Python syntax highlighting"\n'
        'print s\n'
        '```\n', parse_mode='Markdown'
    )


def blogs(update: Update, context: CallbackContext) -> None:
    f = codecs.open('info/blogs.md', encoding='utf-8')
    update.message.reply_text(f.read(), parse_mode='Markdown')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        "1471785144:AAHrsIs6sGPLoGJtilaT7oYlquLyG6jda3o", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("peli", peli))
    dispatcher.add_handler(CommandHandler("telegram", telegram))

    dispatcher.add_handler(CommandHandler("telefon", telefon))
    dispatcher.add_handler(CommandHandler("trobam", trobam))
    dispatcher.add_handler(CommandHandler("estudis", estudis))
    dispatcher.add_handler(CommandHandler("cicles", cicles))
    dispatcher.add_handler(CommandHandler("FPBasica", fpbasica))
    dispatcher.add_handler(CommandHandler("batxillerat", batxillerat))
    dispatcher.add_handler(CommandHandler("batxCIEN", batxCIEN))
    dispatcher.add_handler(CommandHandler("ti1", ti1))
    dispatcher.add_handler(CommandHandler("tic", tic))
    dispatcher.add_handler(CommandHandler("tic4eso", tic4eso))
    dispatcher.add_handler(CommandHandler("programacion", programacion))
    dispatcher.add_handler(CommandHandler("blogs", blogs))
    dispatcher.add_handler(CommandHandler("espais", espais))
    dispatcher.add_handler(CommandHandler(
        "correuelectronic", correuelectronic))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
