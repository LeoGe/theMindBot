# class to remember everything about the running game and keep the bot cleaner

class game():
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.lives = 4
        self.throw_stars = 1
        self.level = 1
        # dict to remember which player has which numbers, chat id of single player to int array :P
        self.player_to_numbers = []
        self.last_number = 0

    def use_throw_stars(self):
        pass

    def draw(self):
        pass

    def check_move(self, new_number, player):
        pass


