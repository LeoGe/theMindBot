from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.error import TelegramError
import logging
from game import Game
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
games = {}
with open('key.txt', 'r') as key_file:
    key=key_file.read().replace('\n', '')

active = False

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Good Evening Ladies and Gentlemen. My name is Harvey. I am your game master this evening. If you want to start a new game just use /go. But first syncronise your thoughts and find you qi. This journey will strain your phsycic abilities to the maximum.')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('You can of course always communicate with me telepathically. Should that not work use these easy commands:\n /help - show this message\n /go - start a new game \n /rules - I will explain the game for all of you that cannot open their third eye yet.')


def move(bot, update):
    chat_id = update.message.chat_id
    if chat_id not in games:
        return
    global active
    print(active)
    if active:
        print(update.message)
        player_id = update.message.from_user.id
        message = update.message.text
        numbers = games[chat_id].player_to_numbers[player_id]
        
        message = int(message)
        if message not in numbers:
            bot.send_message(chat_id,"That was not a valid move! Now you have to start the game again with /ok")
            active = False
            games[chat_id].active_players = []
            return
        smaller_numbers = games[chat_id].check_move(message, player_id)
        if smaller_numbers != 0:
            bot.send_message(chat_id, "Oh no! You have lost a live!")
            if games[chat_id].lives < 0:
                bot.send_message(chat_id, "Ups, you lost the game. You have no lifes left.\n You can start a new game with /go")
                del games[chat_id]
                active = False
                return
            if games.lives == 0:
                bot.send_message(chat_id, "Careful! You are swimming now")
            for player_cnt in smaller_numbers:
                user = bot.get_chat_member(chat_id, player_cnt)
                smaller_numbers_tmp = smaller_numbers[player_cnt]
                if len(smaller_numbers_tmp) == 1:
                    word = number
                else:
                    word = numbers
                string = "I am afraid " + str(user.first_name)+" still has the "+word+" "+str(smaller_numbers_tmp)
                bot.send_message(chat_id, string)
            active = False
            games[chat_id].active_players = []

def status(bot, update):
    chat_id = update.message.chat_id
    if chat_id in games:
        string = "Here is your current game status: You have...\n... "
        string += str(games[chat_id].lives)
        string += " lives left.\n... "
        string += str(games[chat_id].throw_stars)
        string += " throw stars left."
    #string = "Here is your current game status: You have...\n... " + str(games[chat_id].lives) +" lives left \n ... "+str(games[chat_id].throw_stars)" throw stars left"
        bot.send_message(update.message.chat_id, string)
    else:
        bot.send_message(chat_id,"There is currently no game running. You can start it with /go")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)
    

def go(bot, update):
    chat_id = update.message.chat_id
    nr_players = update.message.chat.get_members_count() - 1
    if chat_id in games:
        bot.send_message(chat_id, "There is already a game for this chat. If you want to abort the game use /instantDeath")
        return
    games[chat_id] = Game(nr_players)
    players = update.message.chat.get_administrators()
    #print(len(players))
    if len(players) != nr_players + 1:
        bot.send_message(update.message.chat_id, "Please turn off the setting in the group that everybody is automatically an admin and set everyoe as admin maually so I can reach you.")
    for player in players:
        #print(player.user)
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
    chat_id = update.message.chat_id
    if chat_id not in games:
        bot.send_message(update.message.chat_id, "Please initialise the game first with /go")
        return
    player_id = update.message.from_user.id
    
    if player_id not in games[chat_id].active_players:
        games[chat_id].active_players.append(player_id)
        #print(games[chat_id].active_players)
        #print(games[chat_id].nr_players)
        if len(games[chat_id].active_players) == games[chat_id].nr_players:
        #this might give me some problems if more than one game is running at the same time :D
            bot.send_message(chat_id, "I see you are all ready.")
        #time.sleep(1)
            bot.send_message(chat_id,"3")
        #time.sleep(1)
            bot.send_message(chat_id, "2")
        #time.sleep(1)
            bot.send_message(chat_id,"1")
        #time.sleep(1)
            bot.send_message(chat_id,"GO!")
            global active
            active = True

def stop(bot, update):
    player_id = update.message.from_user.id
    chat_id = update.message.chat_id
    if chat_id not in games:
        bot.send_message(chat_id, "Please start the game first with /go")
        return
    if len(games[chat_id].active_players) < games[chat_id].nr_players:
        bot.send_message(chat_id, "The game is not currently running. Restart ist by typing /ok")
        return
    bot.send_message(chat_id,"I stopped the game. What do you want to do next? Use a Throwstar (/throwstar). I will start the game again when everyone has sent /ok")
    active = False
    games[chat_id].active_players = []
    

def rules(bot, update):
    string = "The game works as follows: I will give you each a random number between 1 and 100. Now you have to write the numbers in the group in the right order without communicating in any way. If you don't you will loose one life. You can pause the game with /stop and then for example agree on using a throwing star, which will releave you of your lowest number. Resume the game with /ok ( Everyone has to write that to resume the game). If you succeed you will get more numbers according to your increasing abilities.\n Good Luck" 
    update.message.reply_text(string)

def main():
    """Start the bot."""
    print("...running...")
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(key)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("go", go))
    dp.add_handler(CommandHandler("rules",rules))
    dp.add_handler(CommandHandler("ok",ok))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("stop", stop))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, move))

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
