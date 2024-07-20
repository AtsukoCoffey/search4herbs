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

sales = SHEET.worksheet('Sheet1')
data = sales.get_all_values()

print(data)

class Player:
    """
    Player's name, HP, items, location_x, location_y
    all the status info
    """
    def __init__(self, name, hp, lv, items):
        self.name = name
        self.hp = hp
        self.lv = lv
        self.items = items

    def call_status(self):
        return f"{player1.name} HP: {player1.hp} Items: {player1.items}"



player1 = input('Please enter your name ( hero\’s name ) alphabet only, 3 or more letters.\n')
player1 = Player(player1, 50, 1, "")
print(player1.call_status())