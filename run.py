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



new_player = input('Please enter your name ( hero’s name - alphabet only, 3 or more letters. )\n')
new_player = Player(new_player, 50, [], 0, 0)
print(new_player.call_status())