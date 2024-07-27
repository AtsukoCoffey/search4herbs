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
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('search4herbs')
# spread sheet
sp_player = SHEET.worksheet('player')
# list data
player_data = sp_player.get_all_values()

TITLE = """
 88888 8
   8   8d8b. .d88b
   8   8P Y8 8.dP'
   8   8   8 `Y88P

.d88b.                     8        8888             8   8            8
YPwww. .d88b .d88 8d8b.d8b 8d8b.    8www.d8b. 8d8b   8www8 .d88b 8d8b 88b. d88b
    d8 8.dP' 8  8 8P  8    8P Y8    8   8' .8 8P     8   8 8.dP' 8P   8  8 `Yb.
`Y88P' `Y88P `Y88 8   `Y8P 8   8    8   `Y8P' 8      8   8 `Y88P 8    88P' Y88P

"""

MAP = """
  @ : Village    M : Mountain
  L : Land       W : Woods      - : Water

   X -6-5-4-3-2-1 0 1 2 3 4 5 6 7 8 9
   Y+--------------------------------
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
FIELD_OP = """
  ---------------------------------
  |"Status"       |"Map"
  |"North" / "N"  |"South" / "S"
  |"East" / "E"   |"West" / "W"
  ---------------------------------
"""

BATTLE_OP = """
  ---------------------------------
  |"Attack"/"A"   |"Run/"R"
  |"Tame"/"T"     |"Surprise"/"S"
  ---------------------------------
"""

hr = "\n---------------------------------------\n"
hr_enter = '\n---------------------------- Press "enter" to continue.\n'


# Controle Printing speed
# Referenced from Stack Overflow and Geeksforgeeks.org -> Credit in README
def print_slow(sentence, speed=0.02):
    '''
    The sentence will be printed out one by one, adjustable speed argument
    c is charactor
    '''
    for c in sentence:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(speed)


def validate_name(name):
    """
    Asking player the valid name input and validation
    """
    try:
        if len(name) < 3:
            raise ValueError(
                f" Please input 3 or more letters. \n \
                You input only {len(name)} letter(s).")
        elif name.isnumeric():
            raise ValueError(" Not all numbers please. 3 or more letters.)\n")
    except ValueError as e:
        print(f" Invalid name. {e} Please try again.\n")
        return False
    return True


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
        Name: {player.name} \n\
        HP:{player.hp} \n\
        Location X:{player.location_x} | Y:{player.location_y} \n\
        Items:{player.items} \n\
        ----------------------------------------\n"


class Monsters:
    """
    Monsters and animals detailed setting
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


def pick_monster():
    """
    Check player's location and send to get_instance function
    and return the monster to battle function.
    """
    if 5 <= player.location_x <= 9:
        if -2 <= player.location_y <= 0:
            monst = get_instance("woods")
    else:
        monst = get_instance("land")
    return monst


def get_instance(zone):
    """
    Sort the monsters by zones using @classmethod and pick one
    This function is called from pick_monster function.
    """
    mons_inst_lis = [monst for monst in Monsters.get(zone)]
    mons_frequen_lis = [monst.frequency for monst in Monsters.get(zone)]
    monst = random.choices(mons_inst_lis, weights=mons_frequen_lis, k=1)
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


def surprise_op():
    """
    Dicide how to surprise the monster
    """
    return random.choices(["hawl", "dash", "mov", "fail"],
    weights=[2, 2, 2, 4], k=1)[0]


def field_event():
    """
    Field battle start. Received argument is only instance's name
    To get the instance call the @classmethod again
    After the first move action send the monster to the battle loop function
    """
    # Deep copy the Monster's instance
    b_monst = deepcopy(pick_monster())

    print_slow(
        f' {player.name} noticed ' + b_monst.name + ' was appeared...\n\n'
    )
    time.sleep(0.5)
    print("  ---------------------------------")
    print(f'  Name: {b_monst.name}')
    print(f'  HP: {b_monst.hp}') 
    print(f'  Attack power: {b_monst.attack}')
    print(f'  Belongings: {b_monst.items}')
    print("  ---------------------------------")

    input(hr_enter)

    # First move
    first_move = move()
    if first_move == "run":
        print_slow(f'\n !! Quickly {b_monst.name} was running away.\n')
    elif first_move == "attack":
        attack_probability = attack()
        if attack_probability == "success":
            print_slow(f'\n Suddenly, {b_monst.name} attacked on you!!\n\n')
            input(hr_enter)
            print_slow(f' You got {b_monst.attack} points damege..\n\n')
            player.hp -= b_monst.attack
            print(f' {player.name} HP : {player.hp}\n\n')
            if player.hp < 1:
                input(hr_enter)
                print_slow(
                    f'\n !!! {player.name} was lost the battle...\n\n', 0.5)
                time.sleep(3)
            else:
                battle_loop(b_monst)
        else:
            print_slow(f'\n Suddenly, {b_monst.name} attacked on you!!\n\n')
            print_slow(f' But failed...Lucky!\n\n')
            input(hr_enter)
            battle_loop(b_monst)
    elif first_move == "falter":
        print_slow(f'\n {b_monst.name} is faltering..\n')
        battle_loop(b_monst)
    input(hr_enter)


def battle_loop(b_monst):
    """
    This loop starts just after the first move action. Iterate until
    player's HP is run out or defeating the monster.
    """
    while True:
        print(" What do you want to do?\n")
        player_op = input(BATTLE_OP)
        if player_op.lower() == "attack" or player_op.lower() == "a":
            attack_probability = attack()
            if attack_probability == "success":
                print_slow(f' {player.name} attacked {b_monst.name}!\n\n')
                print_slow(
                    f' {b_monst.name} got {b_monst.damege} points damege..\n')
                b_monst.hp -= b_monst.damege
                print_slow(f'\n {b_monst.name} HP become {b_monst.hp}')
                input(hr_enter)
                if b_monst.hp > 0:
                    attack_probability = attack()
                    if attack_probability == "success":
                        print_slow(
                            f'\n {b_monst.name} attacked on you!!\n\n')
                        print_slow(
                            f' You got {b_monst.attack} points damege..\n\n')
                        player.hp -= b_monst.attack
                        print_slow(f'{player.name} HP: {player.hp}\n\n')
                        if player.hp < 1:
                            input(hr_enter)
                            print_slow(
                                f' !!! {player.name} was lost the battle...\
                                \n\n', 0.5)
                            time.sleep(3)
                            break
                    else:
                        print_slow(f'\n {b_monst.name} attacked on you!! \n\n')
                        print_slow(f' But failed...Lucky!\n\n')
                        continue
                else:
                    print_slow(
                        f'\n {player.name} was defeated {b_monst.name}!\
                        \n\n')
                    print_slow(f' {player.name} got {b_monst.items}')
                    player.items.setdefault(b_monst.items)
                    break
            else:
                print_slow(f' Ouch!! {player.name} missed the attack..\n\n')
                print_slow(f' {b_monst.name} is about to attack {player.name}')
                input(hr_enter)
                attack_probability = attack()
                if attack_probability == "success":
                    print_slow(f' {b_monst.name} attacked on you!!\n\n')
                    print_slow(f' You got {b_monst.attack} points damege..\n\n')
                    player.hp -= b_monst.attack
                    print(f' {player.name} HP : {player.hp}\n\n')
                    if player.hp < 1:
                        input(hr_enter)
                        print_slow(f' !!! {player.name} was lost the battle...\
                            \n\n', 0.5)
                        time.sleep(3)
                        break
                else:
                    print_slow(f' {b_monst.name} attacked on you!!\n\n ')
                    print_slow(f' But failed...Lucky!\n\n')
                    continue
        elif player_op.lower() == "run" or player_op.lower() == "r":
            attack_probability = attack()
            if attack_probability == "success":
                print_slow(" Escaped successfully!!\n")
                break
            else:
                print_slow(
                    " Unfortunately, couldn't escape successfully..\n\n")
                continue
        elif player_op.lower() == "tame" or player_op.lower() == "t":
            print_slow(f' {player.name} started to tame {b_monst.name}.\n\n')
            print_slow("Don't worry, I won't hurt you...\n\n")
            print_slow(
                f' {b_monst.name} is staring at {player.name} alertly...\n\n')
            print_slow(f' {player.name} sat down and did eye contacting.\n\n')
            attack_probability = attack()
            if attack_probability == "success":
                print_slow(f' {b_monst.name} seems to be calmed down.\n\n')
                print_slow(
                    f' {player.name} found a bisquit in the pocket.\n\
                    and give it to the Monster.\n\n')
                print_slow(f" {b_monst.name} became the player's friend\n\n")
                print_slow(f' {player.name} got {b_monst.name}\n\n')
                player.items.setdefault(b_monst.name)
                break
            else:
                print_slow(
                    " \n\nUnfortunately, It didn't work..\n\n")
                continue
        elif player_op.lower() == "surprise" or player_op.lower() == "s":
            print_slow(f' {player.name} tryed to surprise {b_monst.name}.\n\n')
            how_surp = surprise_op()
            if how_surp == "fail":
                print_slow(
                    f' ....."Whaaaaaaaa!" {player.name} shouted loudly..\n\n')
                print_slow(
                    " \n\nUnfortunately, It didn't work..\n\n")
                continue
            elif how_surp == "hawl":
                print_slow(
                    f' Suddenly {player.name} howled like a wolf.\n\n')
                # print_slow(f' {b_monst.name} scared of it\n')
            elif how_surp == "dash":
                print_slow(
                    f' Suddenly {player.name} dashed towards {b_monst.name}.\n\n')
                # print_slow(f' {b_monst.name} scared of it\n')
            elif how_surp == "mov":
                print_slow(
                    f' Suddenly {player.name} started weird movement...\n\n')
            
            print_slow(f' {b_monst.name} was scared!! Quickly run away.\n\n')
            break
        

def vali_field_achi():
    """
    This validation to check the achievement whether get the items
    and came back to the village
    """
    if any(item == "medicinal herb" for item in player.items):
        if player.location_x == 0:
            if player.location_y == 0:
                print_slow(" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\
                Congratulations!! You came back the village safely!\n\n")
                input(hr_enter)
                print_slow(f' {player.name} rushed to get back home.\n\n\
                Mother: "Ohh! Welcome back {player.name}! \n\n\
                So glad you safely came back.\n\n\
                Thank you! I will give her the medicine now!\n\n')
                input(hr_enter)
                record()


def record():
    """
    Access the spread sheet and record the player's data
    calculate the average hp point last 5 players
    """
    print_slow(" Now let's record your data.\n\n")
    print(player.call_status())
    print_slow(" Accessing the data...\n\n")
    now = datetime.datetime.now()
    data = str(player.name), str(player.hp), str(player.items),
    now.strftime("%x")
    # spread sheet can use append_row but not list can use
    # The datetime object has an unique method for readable strings.
    sp_player.append_row(data)
    player.hp = 0
    print_slow(" Record the data successfully!!...\n\n")


# ==================== Story start from here ====================

print(TITLE)
print_slow(" Welcome to The Search For Herbs game.\n\n")
time.sleep(1)
print_slow(" This is a text based adventure game.\n\n")

# Asking player the valid name and loop. Use valid_name function
while True:
    print_slow(
        "Please enter your name. (This game's hero’s name)\n")
    print_slow("3 or more letters.)\n")
    new_name = input("\n  ")

    if validate_name(new_name):
        print(f"\n\n Welcome {new_name}!")
        break

print(hr)
print_slow(
    "\n This game is going to collect the medicinal herbs to the outside\n\n \
    of the village; where the monsters exist. Through running, fighting or\n\n \
    dealing with monsters complete collecting more than 4 herbs and\n\n \
    safely come back home for the sister. \n\n")

while True:
    print_slow(' Would you like to play?  Type “Yes” or “y” / “No” or “n”\n')
    answer = input("\n ")
    if answer.lower() == "no" or answer.lower() == "n":
        print(f"\n Pity! See you next time {new_name}!\n")
        time.sleep(8)
    elif answer.lower() == "yes" or answer.lower() == "y":
        break
    else:
        print("\n Please input valid keys.\n")

player = Player(new_name, 100, {}, 0, 0)

print_slow('\n You answered "YES" so the story has begun...\n')
time.sleep(0.5)
print(hr)
print_slow(f'\n Somewhere in the magical world,\n\n \
There was a family whose father passed away a few years ago…\n\n \
Young {player.name} and their mother were taking care of \
their sick younger sister.\n\n')
input(hr_enter)
print_slow(f'\n {player.name}: “Hi, mother. She is not well again…” \n\n \
Mother: “…. ( sigh ) I know. But we have run out of medicine.\n\n \
I’ll go out of the village to get the medicinal herbs” \n\n \
{player.name}: “No mother, I’ll go. Please look after her. \
I’ll be back soon.” \n\n \
Mother: “Oh... Please be careful and run away from Monsters…”\n')
input(hr_enter)
print_slow(f'\n Now {player.name} has left their home and walking in \
the village.\n\n Villager: “Hi {player.name}, how’s your sister? \
Where are you going?”\n\n {player.name}: “Hi, I’m going to get \
medicinal herbs. She’s not well again.”\n\n \
Villager: “Oh I’m sorry to hear that. \n\n\
    Hmm, I heard that they were growing around The Northern Mountain.\n\n\
    Or if you want to try, the East Woods monsters might have them."\n\n \
{player.name}: “Thanks!”\n')
input(hr_enter)

print_slow(
    f'\n Now {player.name} is standing just outside of the village.\n')

while player.hp > 0:
    """
    Field event loop. Ask player what's the next move and send to
    field event function. Until player HP runs out.
    When met the Vali_field_achievement() -> exit loop
    """
    vali_field_achi()

    if player.hp > 0:
        print_slow("\n Which direction do you want to go?\n")
        print(' Check your status: "Status" or Look at Map: "Map"')
        print(FIELD_OP)
        answer = input(' ')

        if answer.lower() == "map":
            print(MAP)
            print(
                f'Location X:{player.location_x} | Y:{player.location_y}\n')
        elif answer.lower() == "status":
            print(player.call_status())
        elif answer.lower() == "north" or answer.lower() == "n":
            print_slow(f'\n {player.name} is heading towards north...\n\n')
            time.sleep(1)
            player.location_y += 1
            field_event()
        elif answer.lower() == "east" or answer.lower() == "e":
            print_slow(f'\n {player.name} is heading towards east...\n\n')
            time.sleep(1)
            player.location_x += 1
            field_event()
        elif answer.lower() == "south" or answer.lower() == "s":
            print_slow(f'\n {player.name} is heading towards south...\n\n')
            time.sleep(1)
            player.location_y -= 1
            field_event()
        elif answer.lower() == "west" or answer.lower() == "w":
            print_slow(f'\n {player.name} is heading towards west...\n\n')
            time.sleep(1)
            player.location_x -= 1
            field_event()
        else:
            print(" Invalid input. Please try again.")
        continue

print_slow(f' Thank you for playing this game {player.name}\n\n\n')
