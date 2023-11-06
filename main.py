import requests
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import json

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
    print(f'You got: {critter}')
    value = regenerate_prompt()
    if value is True:
        generate_bug()
    else:
        return

def generate_fish():
    """Generates a random fish"""
    critter = "bitterling"
    print(f'You got: {critter}')
    value = regenerate_prompt()
    if value is True:
        generate_fish()
    else:
        return

def generate_sea_creature():
    """Generates a random sea creature"""
    critter = "seaweed"
    print(f'You got: {critter}')
    value = regenerate_prompt()
    if value is True:
        generate_sea_creature()
    else:
        return

def regenerate_prompt():
    action = inquirer.select(
        message="Would you like to Continue?",
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

def view():
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
        view_bugs()
    if action == "Fish":
        view_fish()
    if action == "Sea Creatures":
        view_sea_creatures()

def view_bugs():
    with open("json/bugs.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for critter_data in data.values():
            name = critter_data["name"]["name-USen"]
            print(name)

def view_fish():
    with open("json/fish.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for critter_data in data.values():
            name = critter_data["name"]["name-USen"]
            print(name)

def view_sea_creatures():
    with open("json/sea.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for critter_data in data.values():
            name = critter_data["name"]["name-USen"]
            print(name)

def search():
    search = inquirer.text(message="Search for a critter:").execute()

def home_nav():
    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Generate Random",
            "Search",
            "View Critters",
            Choice(value=None, name="- EXIT"),
        ],
        default="Generate Name",
    ).execute()
    return action

def main():
    print("Welcome Animal Crossing Critterpedia Library")
    print("use `arrow keys` and `enter` for navigating between options")
    print("------------------------------------------------------------")
    while True:
        action = home_nav()
        if action == "Generate Random":
            generate()
        elif action == "Search":
            search()
        elif action == "View Critters":
            view()
        else:
            break

if __name__ == "__main__":
    main()