import requests
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import json
import time
import sys
from datetime import datetime
from clint.textui import puts, indent, colored

class Date:
    def __init__(self, date, hemisphere):
        self.date = date
        self.hemisphere = hemisphere

    def display_date(self):
        puts(colored.yellow(f"Date: {self.date.date()}"))

    def change_date(self, month):
        pass
def gen_randint():
    """Partner's Microservice"""
    # Microservice will generate random integer between 0-100 and store it in the randint-service text file
    # You can also send other data within the text file if you wish
    f = open("randint-service.txt", "w")
    f.write("run")
    f.close()

def get_randint(type):
    """Partner's Microservice"""
    # Example.py will receive data from communication pipeline and store it in rand_num variable
    loading_bubble(type)
    f = open("randint-service.txt", "r")
    rand_num = f.read()
    f.close()
    return rand_num

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
        return

def generate_bug():
    """Generates a random bug"""
    gen_randint()
    index = get_randint("catching")
    with open("json/bugs.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        critter_name_en = "Nothing :("
        for critter_name, critter_data in data.items():
            if int(index) == critter_data["id"]:
                critter_name_en = critter_data["name"]["name-USen"]
    with indent(4):
        puts(colored.cyan(f'You got: {critter_name_en}'))
    value = regenerate_prompt()
    if value is True:
        generate_bug()
    else:
        return

def generate_fish():
    """Generates a random fish"""
    gen_randint()
    index = get_randint("fishing")
    with open("json/fish.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        critter_name_en = "Nothing :("
        for critter_name, critter_data in data.items():
            if int(index) == critter_data["id"]:
                critter_name_en = critter_data["name"]["name-USen"]
    with indent(4):
        puts(colored.cyan(f'You got: {critter_name_en}'))
    value = regenerate_prompt()
    if value is True:
        generate_fish()
    else:
        return

def generate_sea_creature():
    """Generates a random sea creature"""
    gen_randint()
    index = get_randint("diving")
    with open("json/sea.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        critter_name_en = "Nothing :("
        for critter_name, critter_data in data.items():
            if int(index) == critter_data["id"]:
                critter_name_en = critter_data["name"]["name-USen"]
    with indent(4):
        puts(colored.cyan(f'You got: {critter_name_en}'))
    value = regenerate_prompt()
    if value is True:
        generate_sea_creature()
    else:
        return

def loading_bubble(type: str):
    """Loading bubble"""
    sys.stdout.write(f'\r    {type} ')
    time.sleep(0.5)
    sys.stdout.write(f'\r    {type} ○')
    time.sleep(0.5)
    sys.stdout.write(f'\r    {type} ○ ○')
    time.sleep(0.5)
    sys.stdout.write(f'\r    {type} ○ ○ ○')
    time.sleep(0.5)
    sys.stdout.write('\r' + ' ' * 20 + '\r')

def regenerate_prompt():
    action = inquirer.select(
        message="Would you like to continue?",
        choices=[
            "Yes",
            Choice(value=None, name="- STOP"),
        ],
        default="Yes"
    ).execute()
    if action == "Yes":
        return True
    else:
        return

def view(user_date_obj):
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
        view_bugs(user_date_obj.date)
    if action == "Fish":
        view_fish(user_date_obj.date)
    if action == "Sea Creatures":
        view_sea_creatures(user_date_obj.date)

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
            with indent(4):
                puts(colored.green(f"{critter_name_en}, {critter_time}"))

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
    with indent(4):
        puts(colored.yellow("What is this Animal Crossing Critterpedia Library?"))
    with indent(8):
        puts("Animal Crossing New Horizon is game made by Nintendo. In the game there are three types of critters")
        puts("which the player can catch: bugs, fish, and sea creatures. The availability any individual critter")
        puts("depends on date and time in real life. This library allows users to check the availability of critter on")
        puts("the current day.")
    with indent(4):
        puts(colored.yellow("How to Use:"))
    with indent(8):
        puts("Today's Critters: Display the current critters available today")
        puts("Change Date: Configure the date to a different month or change the hemisphere")
        puts("Search: [insert more information about Search feature]")

def change_display_date(new_date):
    display_date = new_date

def home_nav():
    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Today's Critters",
            "Change Date",
            "Generate Random",
            "Search",
            "About",
            Choice(value=None, name="- EXIT"),
        ],
        default="Generate Name",
    ).execute()
    return action

def main():
    user_date_obj = Date(datetime.now(), "northern")
    puts(colored.yellow("Welcome Animal Crossing Critterpedia Library"))
    puts(colored.yellow("This library displays the currently available critters in the game Animal Crossing New Horizon based on the date. Visit about page for more info."))
    puts(colored.yellow("use `arrow keys` and `enter` for navigating between options"))
    user_date_obj.display_date()
    print("------------------------------------------------------------")
    while True:
        action = home_nav()
        if action == "Today's Critters":
            view(user_date_obj)
        elif action == "Change Date":
            pass
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
