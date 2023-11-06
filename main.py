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
        critter = generate_bug()
    elif action == "Fish":
        critter = generate_fish()
    elif action == "Sea Creatures":
        critter = generate_sea_creature()
    else:
        critter = "Nothing :("

    print(f'You got: {critter}')

def generate_bug():
    """Generates a random bug"""
    return "common butterfly"

def generate_fish():
    """Generates a random fish"""
    return "bitterling"

def generate_sea_creature():
    """Generates a random sea creature"""
    return "seaweed"

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

def view_fish():
    pass

def view_sea_creatures():
    pass

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
            pass
        elif action == "View Critters":
            view()
        else:
            break

if __name__ == "__main__":
    main()