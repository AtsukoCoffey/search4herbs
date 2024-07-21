import gspread
from google.oauth2.service_account import Credentials
import json
import random
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
        return f"----------------------------------------\nName: {new_player.name} \nHP:{new_player.hp} | Items:{new_player.items} \nLocation X:{new_player.location_x} | Y:{new_player.location_y}\n----------------------------------------\n"

def validate_name(name):
    """
    Asking player the valid name input and validation
    """
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
    """
    Asking player the valid name and loop. Use valid_name function
    """
    new_name = input("Please enter your name ( hero’s name - You can use alphabet and marks. 4 or more letters. )\n")
    if validate_name(new_name):
        print(f"Welcome {new_name}")
        break

print("The hero of this game is going to collect medicinal herbs for their sick sister at the outside of the village; where the animals and monsters exist. Running, fighting or dealing with monsters affects the hero’s status. When your health point (HP) became “0”, the game is over. The goal of this game is to complete collecting more than 10 medicinal herbs and safely come back home to heal the hero’s sister. ")

while True:
    answer = input("Would you like to play?  Type “Yes” or “y” / “No” or “n”\n")
    if answer.lower() == "no" or answer.lower() == "n":
        print(f"Pity! See you next time {new_name}!")
    elif answer.lower() == "yes" or answer.lower() == "y":
        break
    else:
        print("Please input valid keys")

new_player = Player(new_name, 50, [], 0, 0)

input(f'You answered "YES" so the story is begging. Press any key to start.')
print(f'-----------------------------------------------------------\nSomewhere in the magical world,\nThere was a family whose father passed away a few years ago…\nYoung {new_player.name} and their mother were taking care of their sick younger sister.\n')
input(f' ----------------------------- Press any key to continue.')
print(f'-----------------------------------------------------------\n{new_player.name} “Hi, mother. She is not well again…”\nMother “…. ( sigh ) I know. But we have run out of medicine. I’ll go out of the village to get the medicinal herbs”\n{new_player.name} “No mother, I’ll go. Please look after her. I’ll be back soon.”\nMother “Please be careful and run away from Monsters…”\n')
input(f' ----------------------------- Press any key to continue.')
print(f'-----------------------------------------------------------\nNow {new_player.name} has left their home and walking in the village.\n\nVillager “Hi {new_player.name}, how’s your sister? Where are you going?”\n{new_player.name} “Hi, I’m going to get medicinal herbs. She’s not well again.”\nVillager “Oh I’m sorry to hear that.  Hmm, I heard that they were growing around The Northern Mountain. Or if you want to fight with monsters, The East Woods monsters might have them. But be careful.”\n{new_player.name} “Thanks!”\n')
input(f' ----------------------------- Press any key to continue.')


class Monsters:
    """
    Monsters and animals event
    """
    instances = []
    def __init__(self, name, hp, attack, items, frequency, zone):
        """
        Monsters and animals status
        """
        self.name = name
        self.hp = hp
        self.attack = attack
        self.items = items
        self.frequency = frequency
        self.zone = zone
        # class attribute to keep track of class instances
        Monsters.instances.append(self)
        
    # Referenced from Stack Overflow's article --> Credit in README file
    # class method to access the get method without any instance
    @classmethod
    def get(cls, value):
        return [inst for inst in cls.instances if inst.zone == value]
        

slime = Monsters("Slime", 3, 6, "stone", 15, "field")
slime2 = Monsters("She-Slime", 4, 7, "gold", 15, "field")
scorpion = Monsters("Iron-Scorpion", 22, 10, "iron", 15, "field")
ghost = Monsters("Ghost", 7, 4, "", 15, "woods")
wolf = Monsters("Bewarewolf", 34, 12, "gold", 10, "field")
skeleton = Monsters("Skeleton", 30, 15, "bone", 10, "field")
dracula = Monsters("Dracky", 6, 9, "medicinal herb", 10, "woods")
dracula2 = Monsters("Drackyma", 10, 15, "medicinal herb", 5, "woods")
slime3 = Monsters("Metal-Slime", 400, 10, "metal", 4, "field")
slime4 = Monsters("King-Slime", 500, 20, "gold", 1, "field")

MAP = """
@ : Village    M : Mountain 
L : Land       W : Woods  - : Water

yX-6-5-4-3-2-1 0 1 2 3 4 5 6 7 8 9
 5 M M M M M M M M M M M M M M M M
 4 M M M M L L L L L L M M M M M M 
 3 L L L L L L L L L L L L L L L L
 2 L L L L L L L L L L L L L L L L
 1 L L L L L L L L L L L L L L L L
 0 L L L L L L @ L L L L L W W W L
-1 L L L L L L L L L L L W W W W L
-2 L L L L L L L L L L L L W W W L
-3 L L L L L L L L L L L L L L L L
-4 - - L L L L - - - - - - - L L L
-5 - - - - - - - - - - - - - - - -
"""

def field_event():
    """
    Get field monsters from monster instances
    """
    field_monster = [monst.name for monst in Monsters.get("field")]
    print(field_monster)


print(f'-----------------------------------------------------------\nNow {new_player.name} is standing just outside of the village.\n')
while True:
    answer = input('Which direction do you want to go?: "North" “N” / "South" “S” / "East" “E” / "West" “W”\nIf you want to look at the map: "Map"\nOr if you want to check your status: "Status"\n')

    if answer.lower() == "map":
        print(MAP)
    elif answer.lower() == "status":
        print(new_player.call_status())
    elif answer.lower() == "north" or answer.lower() == "n":
        new_player.location_y += 1
        field_event()
    elif answer.lower() == "east" or answer.lower() == "e":
        new_player.location_x += 1
        field_event()
    elif answer.lower() == "south" or answer.lower() == "s":
        new_player.location_y -= 1
        field_event()
    elif answer.lower() == "west" or answer.lower() == "w":
        new_player.location_x -= 1
        field_event()
    else:
        print("Invalid input. Please try again.")
