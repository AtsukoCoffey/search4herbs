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
CONGRATS = """
 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\
 Congratulations!!\n\n\
 You came back to the village safely!\n\n
 """
play_move = 0
hr = "\n---------------------------------------\n"
hr_enter = '\n---------------------------- Press "Enter" to continue.\n'


# Controle Printing speed
# Referenced from Stack Overflow and Geeksforgeeks.org -> Credit in README
def pri_s(sentence, speed=0.02):
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
    def __init__(self, name, hp, items, location_x, location_y, friends):
        self.name = name
        self.hp = hp
        self.items = items
        self.location_x = location_x
        self.location_y = location_y
        self.friends = friends

    def call_status(self):
        return f"\n\
        ----------------------------------------\n\
        Name: {player.name} \n\
        HP:{player.hp} \n\
        Location X:{player.location_x} | Y:{player.location_y} \n\
        Items:{player.items} \n\
        Friends:{player.friends} \n\
        ----------------------------------------\n"


class Monsters:
    """
    Monsters and animals detailed setting
    """
    instances = []

    def __init__(self, name, hp, attack, damage, items, frequency, zone):
        """
        Monsters and animals status
        """
        self.name = name
        self.hp = hp
        self.attack = attack
        self.damage = damage
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
Slime = Monsters("Slime", 3, 6, 6, "Medicinal herb", 15, "land")
She_Slime = Monsters("She_Slime", 4, 7, 6, "Gold", 15, "land")
Iron_Scorpion = Monsters("Iron_Scorpion", 12, 9, 6, "Iron", 15, "land")
Ghost = Monsters("Ghost", 12, 4, 6, "Medicinal herb", 15, "woods")
Bewarewolf = Monsters("Bewarewolf", 18, 12, 7, "Medicinal herb", 10, "land")
Skeleton = Monsters("Skeleton", 18, 9, 6, "Bone", 10, "land")
Dracky = Monsters("Dracky", 8, 9, 6, "Medicinal herb", 10, "woods")
Drackyma = Monsters("Drackyma", 10, 10, 7, "Medicinal herb", 5, "woods")
Metal_Slime = Monsters("Metal_Slime", 100, 6, 3, "Metal", 4, "land")
King_Slime = Monsters("King_Slime", 120, 20, 5, "Crown", 1, "land")


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
    # monst was selected only one but still list -> Debug  README
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
    return random.choices(
        ["hawl", "dash", "mov", "fail"], weights=[2, 2, 2, 4], k=1)[0]


def field_event():
    """
    Field battle start. Received argument is only instance's name
    To get the instance call the @classmethod again
    After the first move action send the monster to the battle loop function
    """
    # Deep copy the Monster's instance
    b_monst = deepcopy(pick_monster())

    pri_s(
        f' {player.name} noticed ' + b_monst.name + ' appeared...\n\n'
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
        pri_s(f'\n !! Quickly {b_monst.name} was running away.\n')
    elif first_move == "attack":
        attack_probability = attack()
        if attack_probability == "success":
            pri_s(f'\n Suddenly, {b_monst.name} attacked on you!!\n\n')
            input(hr_enter)
            pri_s(f' You got {b_monst.attack} points damage..\n\n')
            player.hp -= b_monst.attack
            print(f' {player.name} HP : {player.hp}\n\n')
            if player.hp < 1:
                input(hr_enter)
                pri_s(
                    f'\n !!! {player.name} was lost the battle...\n\n', 0.5)
                time.sleep(3)
            else:
                battle_loop(b_monst)
        else:
            pri_s(f'\n Suddenly, {b_monst.name} attacked on you!!\n\n')
            pri_s(f' But failed...Lucky!\n\n')
            input(hr_enter)
            battle_loop(b_monst)
    elif first_move == "falter":
        pri_s(f'\n {b_monst.name} was hesitating..\n')
        battle_loop(b_monst)
    input(hr_enter)


def battle_loop(b_monst):
    """
    This loop starts just after the first move action. Iterate until
    player's HP is run out or defeating the monster.
    """
    while True:
        print(" What do you want to do?\n")
        player_op = input(BATTLE_OP + " ")
        if player_op.lower() == "attack" or player_op.lower() == "a":
            attack_probability = attack()
            if attack_probability == "success":
                pri_s(f' {player.name} attacked {b_monst.name}!\n\n')
                pri_s(
                    f' {b_monst.name} got {b_monst.damage} points damage..\n')
                b_monst.hp -= b_monst.damage
                pri_s(f'\n {b_monst.name} HP became {b_monst.hp}')
                input(hr_enter)
                if b_monst.hp > 0:
                    attack_probability = attack()
                    if attack_probability == "success":
                        pri_s(
                            f'\n {b_monst.name} attacked on you!!\n\n')
                        pri_s(
                            f' You got {b_monst.attack} points damage..\n\n')
                        player.hp -= b_monst.attack
                        pri_s(f' {player.name} HP: {player.hp}\n\n')
                        if player.hp < 1:
                            input(hr_enter)
                            pri_s(
                                f' !!! {player.name} was lost the battle...\
                                \n\n', 0.5)
                            time.sleep(3)
                            break
                    else:
                        pri_s(f'\n {b_monst.name} attacked on you!! \n\n')
                        pri_s(f' But failed...Lucky!\n\n')
                        continue
                else:
                    pri_s(
                        f'\n {player.name} defeated {b_monst.name}!\
                        \n\n')
                    pri_s(f' {player.name} got {b_monst.items}')

                    # If there is no same key in the items dictionary
                    # set new key with value of "0"
                    if b_monst.items not in player.items:
                        player.items[b_monst.items] = 0
                    player.items[b_monst.items] += 1
                    break
            else:
                pri_s(f' Ouch!! {player.name} missed the attack..\n\n')
                pri_s(f' {b_monst.name} was about to attack {player.name}')
                input(hr_enter)
                attack_probability = attack()
                if attack_probability == "success":
                    pri_s(f' {b_monst.name} attacked on you!!\n\n')
                    pri_s(f' You got {b_monst.attack} points damage..\n\n')
                    player.hp -= b_monst.attack
                    print(f' {player.name} HP : {player.hp}\n\n')
                    if player.hp < 1:
                        input(hr_enter)
                        pri_s(f' !!! {player.name} was lost the battle...\
                            \n\n', 0.5)
                        time.sleep(3)
                        break
                else:
                    pri_s(f' {b_monst.name} attacked on you!!\n\n ')
                    pri_s(f' But failed...Lucky!\n\n')
                    continue
        elif player_op.lower() == "run" or player_op.lower() == "r":
            attack_probability = attack()
            if attack_probability == "success":
                pri_s(" Escaped successfully!!\n")
                break
            else:
                pri_s(
                    " Unfortunately, couldn't escape successfully..\n\n")
                continue
        elif player_op.lower() == "tame" or player_op.lower() == "t":
            pri_s(f' {player.name} started to tame {b_monst.name}.\n\n')
            pri_s(" Don't worry, I won't hurt you...\n\n")
            pri_s(
                f' {b_monst.name} was staring at {player.name} alertly...\n\n')
            pri_s(f' {player.name} sat down and did made eye contact.\n\n')
            attack_probability = attack()
            if attack_probability == "success":
                pri_s(f' {b_monst.name} seems calmed down.\n\n')
                pri_s(
                    f' {player.name} found a biscuit in the pocket.\n\
                    And gave it to {b_monst.name}.\n\n')
                pri_s(
                    f" {b_monst.name} became {player.name}'s friend\n\n")

                if b_monst.name not in player.friends:
                    player.friends[b_monst.name] = 0
                player.friends[b_monst.name] += 1
                break
            else:
                pri_s(
                    " \n\nUnfortunately, It didn't work..\n\n")
                continue
        elif player_op.lower() == "surprise" or player_op.lower() == "s":
            pri_s(f' {player.name} tryed to surprise {b_monst.name}.\n\n')
            how_surp = surprise_op()
            if how_surp == "fail":
                pri_s(
                    f' ....."Whaaaaaaaa!" {player.name} shouted loudly..\n\n')
                pri_s(
                    " \n\nUnfortunately, It didn't work..\n\n")
                continue
            elif how_surp == "hawl":
                pri_s(
                    f' Suddenly {player.name} howled like a wolf.\n\n')
            elif how_surp == "dash":
                pri_s(
                    f' Suddenly {player.name} dashed towards {b_monst.name}.')
                print("\n")
            elif how_surp == "mov":
                pri_s(
                    f' Suddenly {player.name} started weird movement...\n\n')
            pri_s(f' {b_monst.name} was scared!! Quickly run away.\n\n')
            break


def vali_field_achi():
    """
    This validation to check the achievement whether get the items
    and came back to the village
    """
    # Check if the "Medicinal herb" is in the items dictionary before validate
    if "Medicinal herb" in player.items and player.items["Medicinal herb"] > 3:
        if player.location_x == 0:
            if player.location_y == 0:
                pri_s(CONGRATS)
                input(hr_enter)
                pri_s(f' {player.name} rushed to get back home.\n\n')
                pri_s(f' Mother: "Ohh! Welcome back {player.name}! \n\n')
                pri_s(" So glad you safely came back.\n\n")
                pri_s(' Thank you! I will give her the medicine now!"\n\n')
                input(hr_enter)
                record()
    else:
        return


def record():
    """
    Access the spread sheet and record the player's data
    calculate the average hp point last 5 players
    """
    pri_s(" Now let's record your data.\n\n")
    print(player.call_status())
    pri_s(" Accessing the data...\n\n")
    now = datetime.datetime.now()
    data = now.strftime("%x"), str(player.name), play_move, str(
        player.hp), str(player.items), str(player.friends),  
    # Spread sheet can use append_row to insert new csv data
    # The datetime object has an unique method for readable strings.
    sp_player.append_row(data)
    player.hp = 0
    pri_s(" Data recorded successfully!!...\n\n")


# ==================== Story start from here ====================

print(TITLE)
pri_s(" Welcome to The Search For Herbs game.\n\n")
time.sleep(1)
pri_s(" This is a text based adventure game.\n\n")

# Asking player the valid name and loop. Use valid_name function
while True:
    pri_s(
        " Please enter your name. (You are the Hero!)\n")
    pri_s(" 3 or more letters.\n")
    new_name = input("\n ")

    if validate_name(new_name):
        print(f"\n\n Welcome {new_name}!")
        break

print(hr)
pri_s(
    "\n In this game you are going to collect Medicinal herbs outside the\
 village; where there are monsters and other scary beasts. You will\
 have to challenge or escape the monsters to survive. Collect 4 herbs\
 and bring them safely back home for your sister.  \n\n")

while True:
    pri_s(' Would you like to play?  Type “Yes” or “Y” / “No” or “N”\n')
    answer = input("\n ")
    if answer.lower() == "no" or answer.lower() == "n":
        print(f"\n Pity! See you next time {new_name}!\n")
        time.sleep(8)
    elif answer.lower() == "yes" or answer.lower() == "y":
        break
    else:
        print("\n Please input valid keys.\n")

player = Player(new_name, 100, {}, 0, 0, {})

pri_s('\n You answered "YES" so the story has begun...\n')
time.sleep(0.5)
print(hr)
pri_s(f'\n Somewhere in the magical world,\n\n\
 There was a family whose father passed away a few years ago…\n\n\
 Young {player.name} and their mother were taking care of\
 their sick younger sister.\n\n')
input(hr_enter)
pri_s(f'\n {player.name}: "Hi, mother. She is not well again…"\n\n\
 Mother: "…. ( sigh ) I know. But we have run out of medicine.\n\n\
 I need to go out of the village to get Medicinal herbs" \n\n\
 {player.name}: "No mother, I will go. Please look after her.\
 I will be back soon."\n\n\
 Mother: "Oh... Please be careful and stay away from Monsters…"\n')
input(hr_enter)
pri_s(f'\n Now {player.name} has left their home and was walking in\
 the village.\n\n Villager: "Hi {player.name}, how is your sister?\
 Where are you going?"\n\n {player.name}: "Hi, I am going to get\
 Medicinal herbs. She is not well again."\n\n\
 Villager: "Oh I am sorry to hear that.\n\n\
    Hmm, I heard there were Medicinal herbs growing around The Northern\
 Mountain.\n\n\
    Or if you want to try, the East Woods monsters might have them."\n\n\
 {player.name}: "Thanks!"\n')
input(hr_enter)

pri_s(
    f'\n Now {player.name} is standing just outside of the village.\n')

while player.hp > 0:
    """
    Field event loop. Ask player what's the next move and send to
    field event function. Until player HP runs out.
    When met the Vali_field_achievement() -> exit loop
    """
    vali_field_achi()

    if player.hp > 0:
        pri_s("\n Which direction do you want to go?\n")
        print(' Check your status: "Status" or Look at Map: "Map"')
        print(FIELD_OP)
        answer = input(' ')

        if answer.lower() == "map":
            print(MAP)
            print(
                f'Location X:{player.location_x} | Y:{player.location_y}\n')
            print(hr_enter)
        elif answer.lower() == "status":
            print(player.call_status())
            print(hr_enter)
        elif answer.lower() == "north" or answer.lower() == "n":
            pri_s(f'\n {player.name} headed North...\n\n')
            play_move += 1
            player.location_y += 1
            field_event()
        elif answer.lower() == "east" or answer.lower() == "e":
            pri_s(f'\n {player.name} headed East...\n\n')
            play_move += 1
            player.location_x += 1
            field_event()
        elif answer.lower() == "south" or answer.lower() == "s":
            pri_s(f'\n {player.name} headed South...\n\n')
            play_move += 1
            player.location_y -= 1
            field_event()
        elif answer.lower() == "west" or answer.lower() == "w":
            pri_s(f'\n {player.name} headed West...\n\n')
            play_move += 1
            player.location_x -= 1
            field_event()
        else:
            print(" Invalid input. Please try again.")
        continue

pri_s(f' Thank you for playing this game {player.name}\n\n\n')
