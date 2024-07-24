import gspread
from google.oauth2.service_account import Credentials
import json
import random
import time
import datetime
import sys
from copy import deepcopy
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

# spread sheet
sp_player = SHEET.worksheet('player')
# list data
player_data = sp_player.get_all_values()

TITLE = """
 _____ _
|_   _| |_  ___
  | | | ' \/ -_)
  |_| |_||_\___|
  _____                     _      ______           _   _           _
 /  ___|                   | |     |  ___|         | | | |         | |
 : `--.  ___  __ _ _ __ ___| |__   | |_ ___  _ __  | |_| | ___ _ __| |__  ___
  `--. \/ _ \/ _` | '__/ __| '_ \  |  _/ _ \| '__| |  _  |/ _ \ '__| '_ \/ __|
 /\__/ /  __/ (_| | | | (__| | | | | || (_) | |    | | | |  __/ |  | |_) \__ |
 \____/ \___|\__,_|_|  \___|_| |_| \_| \___/|_|    \_| |_/\___|_|  |_.__/|___/
"""

hr = "\n\n---------------------------------------\n"
hr_enter = '\n\n---------------------------- Press "enter" to continue.\n'

# Controle Printing speed
# Referenced from Stack Overflow and Geeksforgeeks.org -> Credit in README
def print_slow(sentence, speed=0.01):
    '''
    The sentence will be printed out letter by letter, adjust speed argument
    '''
    for c in sentence:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(speed)


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
        return f"\n\
        ----------------------------------------\n\
        Name: {new_player.name} \n\
        HP:{new_player.hp} \n\
        Location X:{new_player.location_x} | Y:{new_player.location_y} \n\
        Items:{new_player.items} \n\
        ----------------------------------------\n"


def validate_name(name):
    """
    Asking player the valid name input and validation
    """
    try:
        if len(name) < 3:
            raise ValueError(f"Please input more longer name. \
            You input {len(name)} letter(s). 3 or more letters.)\n")
        elif name.isnumeric():
            raise ValueError(f"Not numbers only please. 3 or more letters.)\n")
    except ValueError as e:
        print(f"Invalid name. {e} Please try again.")
        return False
    return True


print(TITLE)
print_slow("Welcome to The Search For Herbs game.\n\n")
time.sleep(1)
print_slow("This is a text based adventure game that is inspired by 80’s\n \
popular RPG game “Dragon Quest”.\n\n")


while True:
    """
    Asking player the valid name and loop. Use valid_name function
    """
    print_slow("Please enter your name. (This game's hero’s name)\n\
3 or more letters.)\n")
    new_name = input("\n")

    if validate_name(new_name):
        print(f"\n\nWelcome {new_name}!")
        break

print(hr)
print_slow("\n\
This game is going to collect the medicinal herbs \n \
to the outside of the village; where the animals and \n \
monsters exist.\n")
input(hr_enter)
print_slow("\n\
Running, fighting or dealing with monsters affects the hero’s status.\n \
The goal of this game is to complete collecting more than 4 medicinal\n \
herbs and safely come back home to heal the hero’s sister. \n\n")

while True:
    print_slow('Would you like to play?  Type “Yes” or “y” / “No” or “n”\n')
    answer = input("\n")
    if answer.lower() == "no" or answer.lower() == "n":
        print(f"\nPity! See you next time {new_name}!\n")
    elif answer.lower() == "yes" or answer.lower() == "y":
        break
    else:
        print("\nPlease input valid keys.\n")

new_player = Player(new_name, 100, {}, 0, 0)

print_slow('\nYou answered "YES" so the story is beggining...\n')
time.sleep(1)
print(hr)
print_slow(f'\nSomewhere in the magical world,\n \
There was a family whose father passed away a few years ago…\n \
Young {new_player.name} and their mother were taking care of \
their sick younger sister.\n')
input(hr_enter)
print_slow(f'\n{new_player.name}: “Hi, mother. She is not well again…” \n\
Mother: “…. ( sigh ) I know. But we have run out of medicine.\n \
I’ll go out of the village to get the medicinal herbs” \n \
{new_player.name}: “No mother, I’ll go. Please look after her. \
I’ll be back soon.” \n\
Mother: “Oh... Please be careful and run away from Monsters…”\n')
input(hr_enter)
print_slow(f'\nNow {new_player.name} has left their home and walking in \
the village.\n\nVillager: “Hi {new_player.name}, how’s your sister? \
Where are you going?”\n\n{new_player.name}: “Hi, I’m going to get \
medicinal herbs. She’s not well again.”\n\n\
Villager “Oh I’m sorry to hear that. \n\
Hmm, I heard that they were growing around The Northern Mountain.\n \
Or if you want to try,\n The East Woods monsters might have them."\n\n \
{new_player.name}: “Thanks!”\n\n')
input(hr_enter)


class Monsters:
    """
    Monsters and animals event
    """
    instances = []

    def __init__(self, name, hp, attack, damege, items, frequency, zone):
        """
        Monsters and animals status
        """
        self.name = name
        self.hp = hp
        self.attack = attack
        self.damege = damege
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

    # Give back the specified instance from it's name
    def get_n(cls, value):
        return [inst for inst in cls.instances if inst.name == value]


# Create monsters instances
# Using capital letter to the python variables is not recomended though
# These are matching to the name attribute because
# Identifying from @class method uses name attribute.
Slime = Monsters("Slime", 3, 6, 6, "medicinal herb", 15, "land")
She_Slime = Monsters("She_Slime", 4, 7, 6, "gold", 15, "land")
Iron_Scorpion = Monsters("Iron_Scorpion", 22, 9, 6, "iron", 15, "land")
Ghost = Monsters("Ghost", 13, 4, 6, "medicinal herb", 15, "woods")
Bewarewolf = Monsters("Bewarewolf", 34, 12, 7, "medicinal herb", 10, "land")
Skeleton = Monsters("Skeleton", 30, 9, 6, "bone", 10, "land")
Dracky = Monsters("Dracky", 6, 9, 6, "medicinal herb", 10, "woods")
Drackyma = Monsters("Drackyma", 10, 10, 6, "medicinal herb", 5, "woods")
Metal_Slime = Monsters("Metal_Slime", 100, 9, 10, "metal", 4, "land")
King_Slime = Monsters("King_Slime", 120, 20, 5, "crown", 1, "land")


MAP = """
@ : Village    M : Mountain
L : Land       W : Woods  - : Water
Check player's location X, Y

 X -6-5-4-3-2-1 0 1 2 3 4 5 6 7 8 9
Y _________________________________
 5| M M M M M M M M M M M M M M M M
 4| M M M M L L L L L L M M M M M M
 3| L L L L L L L L L L L L L L L L
 2| L L L L L L L L L L L L L L L L
 1| L L L L L L L L L L L L L L L L
 0| L L L L L L @ L L L L W W W W W
-1| L L L L L L L L L L L W W W W W
-2| L L L L L L L L L L L W W W W W
-3| L L L L L L L L L L L L L L L L
-4| - - L L L L - - - - - - - L L L
-5| - - - - - - - - - - - - - - - -
"""


def field_event():
    """
    Check player's location for pick monster function,
    and send the monster to battle function.
    """

    if 5 <= new_player.location_x <= 9:
        if -2 <= new_player.location_y <= 0:
            monst = pick_monster("woods")
    else:
        monst = pick_monster("land")

    battle(monst)


def vali_field_achi():
    """
    This validation to check the achievement whether get the items
    and came back to the village
    """
    if any(item == "medicinal herb" for item in new_player.items):
        if new_player.location_x == 0:
            if new_player.location_y == 0:
                print_slow("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n \
                    Congratulations!! You came back safely!\n\n")
                print_slow(f'-----------------------------\n\
                    Mother "Ohh! Thank you {new_player.name}! \n\n\
                    So glad safly came back.\n\n\
                    I will give her the medicine now!')
                input('\n----------------------------- \n\
                    Press "enter" to record the data.\n')
                record()


def pick_monster(zone):
    """
    Sort the monsters by zones from Monsters instances and pick one
    This function is called from field_event function.
    """
    mons_name_lis = [monst.name for monst in Monsters.get(zone)]
    mons_frequen_lis = [monst.frequency for monst in Monsters.get(zone)]
    monst = random.choices(mons_name_lis, weights=mons_frequen_lis, k=1)
    # monst was selected only one but still list ->Debug  README

    return monst[0]


def move():
    """
    Only first move, monster might have a chance to run or attack
    random choice with weights - run=1, attack=1, falter=3
    """
    move = random.choices(("run", "attack", "falter"), weights=[1, 1, 3], k=1)
    return move[0]


def attack():
    """
    Attack might not success all the time. Randomly 1 / 6 fail
    """
    return random.choices(["success", "fail"], weights=[5, 1], k=1)[0]


def battle(monst):
    """
    Field battle start. Received argument is only instance's name
    To get the instance call the @classmethod again
    After the first move action send the monster to the battle loop function
    """
    print_slow(f'{new_player.name} noticed ' + monst + ' was appeared...\n\n')
    time.sleep(1)

    # Take the monster's instance out of the instances list using class method
    battle_monst = deepcopy(Monsters.get_n(Monsters, monst)[0])
    # Deep copy the Monster's instance
    print(f'\nName: {battle_monst.name} ------------------\n\
HP: {battle_monst.hp}\nAttack power: {battle_monst.attack}\n\
Belongings: {battle_monst.items}\n')
    input(hr_enter)

    # First move
    first_move = move()
    if first_move == "run":
        print_slow(f'\n!! Quickly {battle_monst.name} was running away.\n')
    elif first_move == "attack":
        attack_probability = attack()
        if attack_probability == "success":
            print(f'\nSuddenly, {battle_monst.name} attacked on you!!\n\n')
            input(hr_enter)
            print_slow(f'You got {battle_monst.attack} points damege..\n\n')
            new_player.hp -= battle_monst.attack
            print(f'{new_player.name} HP : {new_player.hp}\n\n')

            if new_player.hp < 1:
                input(hr_enter)
                print_slow(f'\nI am so sorry, \
                    {new_player.name} was lost the battle...\n\n')
                time.sleep(3)
            else:
                battle_loop(battle_monst)
        else:
            print(f'\n{battle_monst.name} attacked you!! But failed...Lucky!\n\n')
            input(hr_enter)
            battle_loop(battle_monst)
    elif first_move == "falter":
        print_slow(f'\n{battle_monst.name} is faltering..\n')
        input(hr_enter)
        battle_loop(battle_monst)
    input(hr_enter)


# Battle loop function
def battle_loop(battle_monst):
    """
    This loop starts just after the first move action. Iterate until
    player's HP is run out or defeating the monster.
    """
    while True:
        print("What do you want to do?\n")
        player_op = input('"Attack"/"A", "Run/"R", "Tame"/"T", "Surprise"/"S"\
            \n')
        if player_op.lower() == "attack" or player_op.lower() == "a":
            attack_probability = attack()
            if attack_probability == "success":
                print_slow(f'\n{new_player.name} attacked {battle_monst.name}!\n\n\
                    {battle_monst.name} got {battle_monst.damege} points damege..\
                    \n\n')
                battle_monst.hp -= battle_monst.damege
                print_slow(f'{battle_monst.name} HP become {battle_monst.hp}')
                input(hr_enter)
                if battle_monst.hp > 0:
                    attack_probability = attack()
                    if attack_probability == "success":
                        print_slow(f'\n{battle_monst.name} attacked on you!!\n\
                        You got {battle_monst.attack} points damege..\n')
                        new_player.hp -= battle_monst.attack
                        print_slow(f'{new_player.name} HP: {new_player.hp}\n')
                        input(hr_enter)
                        if new_player.hp < 1:
                            print_slow(f'I am so sorry, {new_player.name} \
                                was lost the battle...\n\n')
                            time.sleep(3)
                            break
                    else:
                        print_slow(f'\n{battle_monst.name} attacked on you!! \
                            But failed...Lucky!\n')
                        continue
                else:
                    print_slow(f'\n\
                        {new_player.name} was defeated {battle_monst.name}!\
                        \n\n')
                    print_slow(f'{new_player.name} got {battle_monst.items}')
                    new_player.items.setdefault(battle_monst.items)
                    break
            else:
                print_slow(f'Ouch!! Missed the attack..\n\n')
                print_slow(f'{battle_monst.name} is about to attack {new_player.name}')
                input(hr_enter)
                attack_probability = attack()
                if attack_probability == "success":
                    print(hr)
                    print(f'{battle_monst.name} attacked on you!!\n\n \
                    You got {battle_monst.attack} points damege..\n\n')
                    new_player.hp -= battle_monst.attack
                    print(f'{new_player.name} HP : {new_player.hp}')
                    if new_player.hp < 1:
                        print_slow(f'\nI am so sorry, \n\
                            {new_player.name} was lost the battle...\n\n')
                        time.sleep(3)
                        break
                else:
                    print(f'{battle_monst.name} attacked on you!!\n\n \
                        But failed...Lucky!\n\n')
                    continue
        if player_op.lower() == "run" or player_op.lower() == "r":
            attack_probability = attack()
            if attack_probability == "success":
                print_slow("Escaped successfully!!\n\n")
                break
            else:
                print_slow("Unfortunately, couldn't escape successfully..\n\n")
                continue


print_slow(f'\nNow {new_player.name} is standing just outside of the \
village.\n')


def record():
    """
    Access the spread sheet and record the player's data
    calculate the average hp point last 5 players 
    """
    print_slow("Now let's record your data.\n\n")
    print(new_player.call_status())
    print_slow("Accessing the data...\n\n")
    current_time = datetime.datetime.now()
    data = str(new_player.name), str(new_player.hp), str(new_player.items)
    # spread sheet can use append_row but not list can use      , current_time
    sp_player.append_row(data)
    print_slow("Record the data successfully!!...\n\n")
    new_player.hp = 0


while new_player.hp > 0:
    """
    Field event loop. Ask player what's the next move and send to
    field event function. Until player HP runs out.
    Before run Validate_field_achievement() for check and exit loop
    """
    vali_field_achi()
    print_slow('\nWhich direction do you want to go?: \n ')
    print('"North" “N” / "South" “S” / "East" “E” / "West" “W”\n \
    If you want to look at the map: "Map"\n \
    Or if you want to check your status: "Status"')
    answer = input('\n')

    if answer.lower() == "map":
        print(MAP)
    elif answer.lower() == "status":
        print(new_player.call_status())
    elif answer.lower() == "north" or answer.lower() == "n":
        print_slow(f'{new_player.name} is heading towards north...\n\n')
        time.sleep(1)
        new_player.location_y += 1
        field_event()
    elif answer.lower() == "east" or answer.lower() == "e":
        print_slow(f'{new_player.name} is heading towards east...\n\n')
        time.sleep(1)
        new_player.location_x += 1
        field_event()
    elif answer.lower() == "south" or answer.lower() == "s":
        print_slow(f'{new_player.name} is heading towards south...\n\n')
        time.sleep(1)
        new_player.location_y -= 1
        field_event()
    elif answer.lower() == "west" or answer.lower() == "w":
        print_slow(f'{new_player.name} is heading towards west...\n\n')
        time.sleep(1)
        new_player.location_x -= 1
        field_event()
    else:
        print("Invalid input. Please try again.")
    continue

print_slow(f'Thank you for playing this game {new_player.name}\n\n\n')
