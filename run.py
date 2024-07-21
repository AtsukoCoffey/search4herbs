import gspread
from google.oauth2.service_account import Credentials
import json
# Every Google account has as an IAM (Identity and Access Management)


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# creds = json.load(open('creds.json'))
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('search4herbs')

player = SHEET.worksheet('player')
player_data = player.get_all_values()

print(player_data[-1])
print("Welcome to The Search For Herbs game.")
print("This is a text based adventure game that is inspired by 80’s popular RPG game “Dragon Quest”.")

class Player:
    """
    Player's name, HP, items, location_x, location_y
    all the status info
    """
    def __init__(self, name, hp, items, location_x, location_y):
        self.name = name
        self.hp = hp
        self.items = items
        self.location_x = location_x
        self.location_y = location_y

    def call_status(self):
        return f"{new_player.name} HP: {new_player.hp} Items: {new_player.items} Location X: {new_player.location_x} Y: {new_player.location_y}"

def validate_name(name):
    try:
        if len(name) < 4:
            raise ValueError(f"Please input more longer name. You input {len(name)} letter(s). - You can use alphabet and some marks and numbers. 4 or more letters. )\n")
        elif name.isnumeric():
            raise ValueError(f"Not numbers only please. - You can use alphabet and some marks and numbers. 4 or more letters. )\n")
    except ValueError as e:
        print(f"Invalid name. {e} Please try again.")
        return False
    return True

while True:
    new_name = input("Please enter your name ( hero’s name - You can use alphabet and marks. 4 or more letters. )\n")
    if validate_name(new_name):
        print(f"Welcome {new_name}")
        break

print("The hero of this game is going to collect medicinal herbs for their sick sister at the outside of the village; where the animals and monsters exist. Running, fighting or dealing with monsters affects the hero’s status. When your health point (HP) became “0”, the game is over, so try to save your health. The goal of this game is to complete collecting more than 10 medicinal herbs and safely come back home to heal the hero’s sister. ")

while True:
    answer = input("Would you like to play?  Type “Yes” or “y” / “No” or “n”\n")
    if answer.lower() == "no" or answer.lower() == "n":
        print(f"Pity! See you next time {new_name}!")
    elif answer.lower() == "yes" or answer.lower() == "y":
        break
    else:
        print("Please input valid keys")




new_player = Player(new_name, 50, [], 0, 0)
print(new_player.call_status())