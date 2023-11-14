import requests
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import json
import time
import sys
from datetime import datetime

class Date:
    def __init__(self, date):
        self.date = date

    def display_date(self):
        print(f"Date: {self.date}")

    def change_date(self, month):
        pass


def generate():
    """Generates a random critter depending on which option the user selects"""
    action = inquirer.select(
        message="Choose Critter Type",
        choices=[
            "Bugs",
            "Fish",
            "Sea Creatures",
            Choice(value=None, name="← BACK"),
        ],
        default="Bugs"
    ).execute()
    if action == "Bugs":
        generate_bug()
    elif action == "Fish":
        generate_fish()
    elif action == "Sea Creatures":
        generate_sea_creature()
    else:
        print("Nothing :(")


def generate_bug():
    """Generates a random bug"""
    critter = "common butterfly"
    loading_bubble("catching")
    print(f'You got: {critter}')
    value = regenerate_prompt()
    if value is True:
        generate_bug()
    else:
        return

def generate_fish():
    """Generates a random fish"""
    critter = "bitterling"
    loading_bubble("fishing")
    print(f'You got: {critter}')
    value = regenerate_prompt()
    if value is True:
        generate_fish()
    else:
        return

def generate_sea_creature():
    """Generates a random sea creature"""
    critter = "seaweed"
    loading_bubble("diving")
    print(f'You got: {critter}')
    value = regenerate_prompt()
    if value is True:
        generate_sea_creature()
    else:
        return

def loading_bubble(type: str):
    """Loading bubble"""
    sys.stdout.write(f'\r{type} ')
    time.sleep(0.5)
    sys.stdout.write(f'\r{type} ○')
    time.sleep(0.5)
    sys.stdout.write(f'\r{type} ○ ○')
    time.sleep(0.5)
    sys.stdout.write(f'\r{type} ○ ○ ○')
    time.sleep(0.5)
    sys.stdout.write('\r')


def regenerate_prompt():
    action = inquirer.select(
        message="Would you like to continue?",
        choices=[
            "Yes",
            Choice(value=None, name="- STOP"),
        ],
        default="Bugs"
    ).execute()
    if action == "Yes":
        return True
    else:
        return

def view(user_date):
    action = inquirer.select(
        message="Choose Critter Type",
        choices=[
            "Bugs",
            "Fish",
            "Sea Creatures",
            Choice(value=None, name="← BACK"),
        ],
        default="Bugs"
    ).execute()
    if action == "Bugs":
        view_bugs(user_date)
    if action == "Fish":
        view_fish(user_date)
    if action == "Sea Creatures":
        view_sea_creatures(user_date)

def print_available_critters(user_date, data):
    for critter_name, critter_data in data.items():
        if (
                user_date.month in critter_data["availability"]["month-array-northern"]
                and user_date.hour in critter_data["availability"]["time-array"]
        ):
            critter_name_en = critter_data["name"]["name-USen"]
            critter_time = critter_data["availability"]["time"]
            if critter_time == "":
                critter_time = "all day"
            print(f"{critter_name_en}, {critter_time}")

def view_bugs(user_date):
    with open("json/bugs.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        print_available_critters(user_date, data)

def view_fish(user_date):
    with open("json/fish.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        print_available_critters(user_date, data)

def view_sea_creatures(user_date):
    with open("json/sea.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        print_available_critters(user_date, data)

def search():
    print(" * Read the About page for more info")
    search = inquirer.text(message="Search for a critter:").execute()

def about():
    print("[insert more information about Search feature]")

def change_display_date(new_date):
    display_date = new_date

def home_nav():
    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Today's Critters",
            "Generate Random",
            "Search",
            "About",
            Choice(value=None, name="- EXIT"),
        ],
        default="Generate Name",
    ).execute()
    return action

def main():
    user_date_obj = Date(datetime.now())
    print("Welcome Animal Crossing Critterpedia Library")
    user_date_obj.display_date()
    print("use `arrow keys` and `enter` for navigating between options")
    print("------------------------------------------------------------")
    while True:
        action = home_nav()
        if action == "Today's Critters":
            view(user_date_obj.date)
        elif action == "Generate Random":
            generate()
        elif action == "Search":
            search()
        elif action == "About":
            about()
        else:
            break

if __name__ == "__main__":
    main()
