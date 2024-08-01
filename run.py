import gspread   # Google spread sheet for save players data
from google.oauth2.service_account import Credentials
import json   # Convert ot import data to access Google API
import random   # Used for many functions in this game
import time   # Used for time.sleep() and slow printing (pri_s)
import datetime   # Add the current date when recording player's new data
import sys   # Used for slow printing (pri_s)
from copy import deepcopy   # used for the battle Monster

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
# Spread sheet - records players data
sp_player = SHEET.worksheet('player')
# From spread sheet, extracted as list format
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
   5| L L L L M M M M M M M M L L L L
   4| L L L L L L L L L L L L L L L L
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
play_move = 0   # Counter of player's move. Lower moves means better score.
hr = "\n---------------------------------------\n"
hr_enter = '\n---------------------------- Press "Enter" to continue.\n'


# Referenced from Stack Overflow and Geeksforgeeks.org -> Credit in README
def pri_s(sentence, speed=0.0):
    '''
    The sentences will be printed out one by one, with an adjustable
    speed argument. c (character)
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
            raise ValueError(f" You input only {len(name)} letter(s).")
        elif name.isnumeric():
            raise ValueError(" Not all numbers please.)\n")
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
slime = Monsters("Slime", 3, 3, 6, "Stone", 15, "land")
she_slime = Monsters("She Slime", 4, 4, 6, "Gold", 15, "land")
iron_scorpion = Monsters("Iron Scorpion", 12, 5, 6, "Iron", 15, "land")
ghost = Monsters("Ghost", 12, 3, 6, "Medicinal herb", 15, "woods")
bewarewolf = Monsters("Bewarewolf", 18, 6, 7, "Large fang", 10, "land")
skeleton = Monsters("Skeleton", 18, 6, 6, "Bone", 10, "land")
dracky = Monsters("Dracky", 8, 5, 6, "Medicinal herb", 10, "woods")
drackyma = Monsters("Drackyma", 10, 16, 7, "Medicinal herb", 5, "woods")
metal_slime = Monsters("Metal Slime", 25, 6, 3, "Metal", 4, "land")
king_slime = Monsters("King Slime", 40, 10, 5, "Crown", 1, "land")


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
    Only first battle move, monster might have a chance to run or attack
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
    After the first battle move send the monster to the battle loop function
    """
    # Deep copy the Monster's instance
    b_monst = deepcopy(pick_monster())

    pri_s(   # Print Monster's status
        f' {player.name} noticed ' + b_monst.name + ' appeared...\n\n')
    time.sleep(0.5)
    print("  ---------------------------------")
    print(f'  Name: {b_monst.name}')
    print(f'  HP: {b_monst.hp}')
    print(f'  Attack power: {b_monst.attack}')
    print(f'  Belongings: {b_monst.items}')
    print("  ---------------------------------")
    input(hr_enter)

    first_move = move()   # Monster's first action - run, attack or squaringup
    if first_move == "run":   # Monster - run
        pri_s(f'\n !! Quickly {b_monst.name} was running away.\n')
    elif first_move == "attack":   # Monster - attack thier first move
        success_rate = attack()   # calculate the success rate
        if success_rate == "success":
            pri_s(f'\n Suddenly, {b_monst.name} attacked on you!!\n\n')
            input(hr_enter)
            pri_s(f' You got {b_monst.attack} points damage..\n\n')
            player.hp -= b_monst.attack
            print(f' {player.name} HP : {player.hp}\n\n')
            input(hr_enter)
            if player.hp < 1:   # When player was defeated by monster
                lost_status()
            else:   # If player survives the first attack,
                battle_loop(b_monst)   # bring this monster into battle_loop()
        else:   # Monster - fail thier first move
            pri_s(f'\n Suddenly, {b_monst.name} attacked on you!!\n\n')
            pri_s(f' But failed...Lucky!\n\n')
            input(hr_enter)
            battle_loop(b_monst)   # bring this monster into battle_loop()
    elif first_move == "falter":   # Monster - hesitating thier first move
        pri_s(f'\n {b_monst.name} was squaring up to you.\n\n')
        battle_loop(b_monst)
    input(hr_enter)


def battle_loop(b_monst):
    """
    This loop starts just after the first battle move. Iterate until
    player's HP runs out or player defeats the monster. Ask player
    next action. Attack, Run, Tame, Surprise
    """
    while True:
        print(" What do you want to do?\n")
        player_op = input(BATTLE_OP + "\n ")
        player_op = player_op.lower()
        try:   # If empty value or invalid key raise error
            if player_op not in (
                "attack", "a", "run", "r", "tame", "t", "surprise", "s"
            ):
                raise ValueError(" Invalid input.")
        except ValueError as e:
            pri_s(f'{e} Please try again.')
        if player_op in ("attack", "a"):   # If player choose "Attack"
            success_rate = attack()   # calculate success rate for the attack
            if success_rate == "success":
                pri_s(f' {player.name} attacked {b_monst.name}!\n\n')
                pri_s(
                    f' {b_monst.name} got {b_monst.damage} points damage..\n')
                b_monst.hp -= b_monst.damage
                pri_s(f'\n {b_monst.name} HP became {b_monst.hp}')
                input(hr_enter)
                if b_monst.hp > 0:   # If Monster wasn't defeated, their turn.
                    success_rate = attack()   # Monster's return attack rate
                    if success_rate == "success":
                        pri_s(
                            f'\n {b_monst.name} attacked on you!!\n\n')
                        pri_s(
                            f' You got {b_monst.attack} points damage..\n\n')
                        player.hp -= b_monst.attack
                        pri_s(f' {player.name} HP: {player.hp}\n\n')
                        input(hr_enter)
                        if player.hp < 1:   # When player was defeated
                            lost_status()
                            break
                    else:   # Monsters sometimes fail their attack too
                        pri_s(f'\n {b_monst.name} attacked on you!! \n\n')
                        pri_s(f' But failed...Lucky!\n\n')
                        continue
                else:   # When player defeats the monster
                    pri_s(f'\n {player.name} defeated {b_monst.name}!\n\n')
                    pri_s(f' {player.name} got {b_monst.items}')
                    # If there is no same key in the player's items
                    # set new key with value of "0"
                    if b_monst.items not in player.items:
                        player.items[b_monst.items] = 0
                    player.items[b_monst.items] += 1
                    break
            else:   # Player sometimes misses the attack by success rate
                pri_s(f' Ouch!! {player.name} missed the attack..\n\n')
                pri_s(f' {b_monst.name} was about to attack {player.name}')
                input(hr_enter)
                success_rate = attack()   # Monster's return attack rate
                if success_rate == "success":
                    pri_s(f' {b_monst.name} attacked on you!!\n\n')
                    pri_s(f' You got {b_monst.attack} points damage..\n\n')
                    player.hp -= b_monst.attack
                    print(f' {player.name} HP : {player.hp}\n\n')
                    input(hr_enter)
                    if player.hp < 1:   # When player was defeated by monster
                        lost_status()
                        break
                else:   # Sometimes player misses, then Monster misses too.
                    pri_s(f' {b_monst.name} attacked on you!!\n\n ')
                    pri_s(f' But failed...Lucky!\n\n')
                    continue
        elif player_op in ("run", "r"):   # If player choose "Run"
            success_rate = attack()   # calculate success rate for the run
            if success_rate == "success":
                pri_s(" Escaped successfully!!\n")
                break
            else:
                pri_s(
                    " Unfortunately, couldn't escape successfully..\n\n")
                continue
        elif player_op in ("tame", "t"):   # If player choose "Tame"
            pri_s(f' {player.name} started to tame {b_monst.name}.\n\n')
            pri_s(" Don't worry, I won't hurt you...\n\n")
            pri_s(
                f' {b_monst.name} was staring at {player.name} alertly...\n\n')
            pri_s(f' {player.name} sat down and made eye contact.\n\n')
            success_rate = attack()   # calculate success rate for the tame
            if success_rate == "success":
                pri_s(f' {b_monst.name} appears to have calmed down.\n\n')
                pri_s(
                    f' {player.name} found a biscuit in the pocket.\n\
                    And gave it to {b_monst.name}.\n\n')
                pri_s(
                    f" {b_monst.name} became {player.name}'s friend\n\n")
                # If there is no same key in the player's friends
                # set new key with value of "0"
                if b_monst.name not in player.friends:
                    player.friends[b_monst.name] = 0
                player.friends[b_monst.name] += 1
                break
            else:
                pri_s(
                    " \n\nUnfortunately, It didn't work..\n\n")
                continue
        elif player_op in ("surprise", "s"):   # If player choose "Surprise"
            pri_s(f' {player.name} tryed to surprise {b_monst.name}.\n\n')
            how_surp = surprise_op()   # calculate success rate for surprise
            if how_surp == "fail":   # Fail to surprise
                pri_s(
                    f' ....."Whaaaaaaaa!" {player.name} shouted loudly..\n\n')
                pri_s(
                    "\n\n Unfortunately, It didn't work..\n\n")
                continue
            elif how_surp == "hawl":   # Surprise version 1
                pri_s(
                    f' Suddenly {player.name} howled like a wolf.\n\n')
            elif how_surp == "dash":   # Surprise version 2
                pri_s(
                    f' Suddenly {player.name} dashed towards {b_monst.name}.')
                print("\n")
            elif how_surp == "mov":   # Surprise version 3
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
    if "Medicinal herb" in player.items and player.items["Medicinal herb"] > 1:
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
    pri_s(f'You completed the game within {play_move} moves.\n')
    pri_s(" Accessing the data...\n\n")
    now = datetime.datetime.now()
    data = now.strftime("%x"), str(player.name), play_move, str(
        player.hp), str(player.items), str(player.friends),
    # Spread sheet can use append_row to insert new csv data
    # The datetime object has an unique method for readable strings.
    sp_player.append_row(data)
    player.hp = 0
    pri_s(" Data recorded successfully!!...\n\n")
    input(hr_enter)


def map_vali(direction):
    """
    This function stops the player to go outside of the map
    """
    try:
        if (
            direction in ("north", "n") and player.location_y == 5 or
            direction in ("south", "s") and player.location_y == -5 or
            direction in ("east", "e") and player.location_x == 9 or
            direction in ("west", "w") and player.location_x == -6
        ):
            raise IndexError(" Please stay inside the Map!\n")
    except IndexError as e:
        pri_s(f"{e}")
        return False

    return True


def lost_status():
    """
    When player lost the battle, shows score and message
    """
    pri_s(
        f' !!! {player.name} was lost the battle...\n\n', 0.1)
    time.sleep(3)
    pri_s(" This is your score for this round. Fair play!")
    print(player.call_status())


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
    " In this game you are going to collect Medicinal herbs outside the\n\n")
pri_s(
    " village; where there are monsters and other scary beasts. You will\n\n")
pri_s(
    " have to challenge or escape the monsters to survive.\n\n")
pri_s(
    " Collect 4 herbs and bring them safely back home for your sister.\n\n")

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
\n\n\
    Mountain. Or the East Woods monsters might have them."\n\n\
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
    pri_s("\n Which direction do you want to go?\n")
    print(' Check your status: "Status" or Look at Map: "Map"')
    print(FIELD_OP)
    answer = input(' ')
    answer = answer.lower()
    try:
        if answer not in (
            "status", "map", "north", "n", "east", "e", "south", "s", "west",
            "w"
        ):
            raise ValueError(" Invalid input.")
    except ValueError as e:
        pri_s(f'{e} Please try again.')
        continue
    if answer == "map":
        print(MAP)
        print(
            f'  Location X:{player.location_x} | Y:{player.location_y}\n')
        input(hr_enter)
    elif answer == "status":
        print(player.call_status())
        input(hr_enter)
    elif map_vali(answer):   # If map validation is True execute below
        play_move += 1
        # Medicinal Herb growing position in Northern mountain
        if (
            player.location_y == 5 and
            -2 <= player.location_x <= 5 and
            answer in ("east", "e")
        ):
            player.location_x += 1
            pri_s(
                f' !!! {player.name} found a Medicinal herb !!!\n\n')
            pri_s(f' {player.name} got a Medicinal herb!\n\n')
            # Check if the herb is already exist, if not add the key
            if "Medicinal herb" not in player.items:
                player.items["Medicinal herb"] = 0
            player.items["Medicinal herb"] += 1
        elif (
            player.location_y == 5 and
            -2 <= player.location_x <= 5 and
            answer in ("west", "w")
        ):
            player.location_x -= 1
            pri_s(
                f' !!! {player.name} found a Medicinal herb !!!\n\n')
            pri_s(f' {player.name} got a Medicinal herb!\n\n')
            # Check if the herb is already exist, if not add the key
            if "Medicinal herb" not in player.items:
                player.items["Medicinal herb"] = 0
            player.items["Medicinal herb"] += 1
        elif answer in ("north", "n"):
            pri_s(f'\n {player.name} headed North...\n\n')
            player.location_y += 1
        elif answer in ("east", "e"):
            pri_s(f'\n {player.name} headed East...\n\n')
            player.location_x += 1
        elif answer in ("south", "s"):
            pri_s(f'\n {player.name} headed South...\n\n')
            player.location_y -= 1
        elif answer in ("west", "w"):
            pri_s(f'\n {player.name} headed West...\n\n')
            player.location_x -= 1

        field_event()
    vali_field_achi()


def get_players_data():
    """
    Collects best 5 players data in all the data
    1. list of colum(3), 2. create dictionary of colm(3) and index
    """
    colm_move = sp_player.col_values(3)
    # Add index numbers and make a list of tuple -> Credit "How to convert.."
    colm_lis = enumerate(colm_move)
    # lambda argument x indicate second position of tuple - sorted by x value
    move_sorted = sorted(colm_lis, key=lambda x: int(x[1]))
    # move_sorted is like this data [(3, '5'), (0, '6'), (8, '7'), (1, '8'), )]
    # Stores best players index numbers
    player_1_i = move_sorted[0][0]
    player_2_i = move_sorted[1][0]
    player_3_i = move_sorted[2][0]
    player_4_i = move_sorted[3][0]
    player_5_i = move_sorted[4][0]

    pri_s(" These are the Top 5 best players.\n\n")
    pri_s(
        f"""
 The record is {player_data[player_1_i][2]} moves\
 by {player_data[player_1_i][1]} on {player_data[player_1_i][0]}\n\n"""
    )
    input(hr_enter)
    pri_s(
        f"""No.1-------------------------------------------
 {player_data[player_1_i][0]}, {player_data[player_1_i][1]},
 {player_data[player_1_i][2]} moves, HP {player_data[player_1_i][3]}
 Items {player_data[player_1_i][4]}\n Friends {player_data[player_1_i][5]}\n
No.2-------------------------------------------
 {player_data[player_2_i][0]}, {player_data[player_2_i][1]},
 {player_data[player_2_i][2]} moves, HP {player_data[player_2_i][3]}
 Items {player_data[player_2_i][4]}\n Friends {player_data[player_2_i][5]}\n
No.3-------------------------------------------
 {player_data[player_3_i][0]}, {player_data[player_3_i][1]},
 {player_data[player_3_i][2]} moves, HP {player_data[player_3_i][3]}
 Items {player_data[player_3_i][4]}\n Friends {player_data[player_3_i][5]}\n
No.4-------------------------------------------
 {player_data[player_4_i][0]}, {player_data[player_4_i][1]},
 {player_data[player_4_i][2]} moves, HP {player_data[player_4_i][3]}
 Items {player_data[player_4_i][4]}\n Friends {player_data[player_4_i][5]}\n
No.5-------------------------------------------
 {player_data[player_5_i][0]}, {player_data[player_5_i][1]},
 {player_data[player_5_i][2]} moves, HP {player_data[player_5_i][3]}
 Items {player_data[player_5_i][4]}\n Friends {player_data[player_5_i][5]}\n
    """)


get_players_data()
input(hr_enter)
pri_s(f' Thank you for playing this game {player.name}\n\n\n')
