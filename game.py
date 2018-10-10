# class to remember everything about the running game and keep the bot cleaner
# there is no error handling in here. Nor does this class implement a lot of rules. More a way to save the status of the game
from random import sample

class Game():
    def __init__(self, number_players):
        self.nr_players = number_players
        self.active_players = []
        self.lives = 4
        self.throw_stars = 1
        self.level = 1
        # dict to remember which player has which numbers, chat id of single player to int array :P
        self.player_to_numbers = {}
        self.last_number = 0

    def no_nrs_left(self):
        for player in self.player_to_numbers:
            #print("No numbers left test")
            #print(self.player_to_numbers[player])
            if self.player_to_numbers[player] != []:
                return False
        return True

    def use_throwstar(self):
        throw_away = {}
        for player_id in self.player_to_numbers:
            if len(self.player_to_numbers[player_id])>0:
                min_number = min(self.player_to_numbers[player_id])
                throw_away[player_id] = min_number
                self.player_to_numbers[player_id].remove(min_number)

        return throw_away

    def draw(self):
        rand_arr = sample(range(1,100), self.level * self.nr_players)
        i = 0
        #print(rand_arr)
        for player_id in self.player_to_numbers:
            self.player_to_numbers[player_id] = rand_arr[i*self.level:(i+1)*self.level]
            i = i+1


    def check_move(self, new_number, player_id):
        self.player_to_numbers[player_id].remove(new_number)
        self.last_number = new_number
        smaller_numbers = {}
        for player_cnt in self.player_to_numbers:
            temp = [x for x in self.player_to_numbers[player_cnt] if x < self.last_number]
            if temp:
                smaller_numbers[player_cnt] = temp
                for num in temp:
                    self.player_to_numbers[player_cnt].remove(num)
        if len(smaller_numbers) > 0:
            self.lives = self.lives -1
            print("Fail")
            return smaller_numbers
        print("Success")
        return 0

