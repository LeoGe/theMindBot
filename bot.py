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

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.error import TelegramError
import logging
from game import Game

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
games = {}

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
    chat_id = update.message.chat_id
    nr_players = update.message.chat.get_members_count() - 1
    games[chat_id] = Game(nr_players)
    players = update.message.chat.get_administrators()
    print(len(players))
    if len(players) != nr_players + 1:
        bot.send_message(update.message.chat_id, "Please turn off the setting in the group that everybody is automatically an admin and set everyoe as admin maually so I can reach you.")
    for player in players:
        print(player.user)
        if not player.user.is_bot:
            games[chat_id].player_to_numbers[player.user.id]=[]
    games[chat_id].draw()
    #bot.send_message(players[2].user.id,str(games[chat_id].player_to_numbers[players[2].user.id]))
    try:

        for player in games[chat_id].player_to_numbers:
            message = "Your numbers are:\n " + str(games[chat_id].player_to_numbers[player])
            bot.send_message(player, message)
    except TelegramError:
        update.message.reply_text("There is a small problem with that. At least one person in this group has not messaged me personally. Unfortunately I am under a curse, so you have to contact me first before I can contact you. So please say hello to me and try again and I will give you your destined numbers. And to everyboday else: Please forget everything I have already sent you.")
        del games[chat_id]
        return
    bot.send_message(update.message.chat_id, "I have sent everyone of you your numbers. If you are ready please write /ok and I will start the gane")

def ok(bot, update):
    if not games[chat_id]:
        bot.send_message(update.message.chat_id, "Please initialise the game first with /go")
        return
    player_id = update.message.from_user    
    

def rules(bot, update):
    string = "The game works as follows: I will give you each a random number between 1 and 100. Now you have to write the numbers in the group in the right order without communicating in any way. If you don't you will loose one life. You can pause the game with /pause and then for example agree on using a throwing star, which will releave you of your lowest number. Resume the game with /resume ( Everyone has to write that to resume the game). If you succeed you will get more numbers according to your increasing abilities.\n Good Luck" 
    update.message.reply_text(string)

def main():
    """Start the bot."""
    print("...running...")
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
