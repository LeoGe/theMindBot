#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Good Evening Ladies and Gentlemen. My name is Harvey. I am your game master this evening. If you want to start a new game just use /go. But first syncronise your thoughts and find you qi. This journey will strain your phsycic abilities to the maximum.')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('You can of course always communicate with me telepathically. Should that not work use these easy commands:\n /help - show this message\n /go - start a new game \n /rules - I will explain the game for all of you that cannot open their third eye yet.')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def go(bot, update):
    pass

def rules(bot, update):
    string = "The game works as follows: I will give you each a random number between 1 and 100. Now you have to write the numbers in the group in the right order without communicating in any way. If you don't you will loose one life. You can pause the game with /pause and then for example agree on using a throwing star, which will releave you of your lowest number. Resume the game with /resume ( Everyone has to write that to resume the game). If you succeed you will get more numbers according to your increasing abilities.\n Good Luck" 
    update.message.reply_text(string)

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("673160118:AAEkXqLr84VzRuhSnRRwCP6X0NBnpBEp5bI")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("go", go))
    dp.add_handler(CommandHandler("rules",rules))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

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
