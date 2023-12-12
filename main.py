from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import json
import time
import sys
from datetime import datetime
from clint.textui import puts, indent, colored
import calendar

class Date:
    """Object that represents user's current date and hemisphere"""
    def __init__(self, date, hemisphere):
        self.date = date
        self.hemisphere = hemisphere

    def display_date(self):
        """Display the user's date"""
        puts(colored.yellow(f"Date: {self.date.date()}"))

    def display_hemisphere(self):
        """Display the user's hemisphere"""
        puts(colored.yellow(f"Hemisphere: {self.hemisphere.capitalize()}"))

    def change_date(self, new_date):
        """Reassign user's date"""
        self.date = new_date

    def change_hemisphere(self, new_hemisphere):
        """Reassign user's hemisphere"""
        self.hemisphere = new_hemisphere.lower()

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
    category = inquirer.select(
        message="Choose Critter Type",
        choices=[
            "Bugs",
            "Fish",
            "Sea Creatures",
            Choice(value=None, name="← BACK"),
        ],
        default="Bugs"
    ).execute()
    if category == "Sea Creatures":
        category = "Sea"
    elif category is None:
        return

    generate_critter(category)

def generate_critter(category):
    """Simulates catching a random critter based on critter type"""
    gen_randint()
    if category == "Bugs":
        method = "catching"
    elif category == "Fish":
        method = "fishing"
    elif category == "Sea":
        method = "diving"

    index = get_randint(f"{method}")
    with open(f"json/{category.lower()}.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        critter_name_en = "nothing :("
        for critter_name, critter_data in data.items():
            if int(index) == critter_data["id"]:
                critter_name_en = critter_data["name"]["name-USen"]
    with indent(4):
        puts(colored.cyan(f'You got: {critter_name_en}'))

    action = inquirer.select(
        message="Select an action",
        choices=[
            "Generate Again",
            "Search",
            Choice(value=None, name="← BACK"),
        ],
        default="Yes"
    ).execute()
    if action == "Generate Again":
        generate_critter(category)
    if action == "Search":
        search()
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

def available_critters(user_date_obj):
    """Prompts user by what critter type they want to view available critters"""
    category = inquirer.select(
        message="Choose Critter Type",
        choices=[
            "Bugs",
            "Fish",
            "Sea Creatures",
            Choice(value=None, name="← BACK"),
        ],
        default="Bugs"
    ).execute()
    if category == "Sea Creatures":
        category = "Sea"
    elif category is None:
        return

    with open(f"json/{category.lower()}.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        print_available_critters(user_date_obj.date, user_date_obj.hemisphere, data)
    with indent(4):
        user_date_obj.display_date()
        user_date_obj.display_hemisphere()

    # Backtracking prompts
    action = inquirer.select(
        message="Select an action",
        choices=[
            "View Other Critter Types",
            "Search",
            Choice(value=None, name="← BACK"),
        ],
        default="Yes"
    ).execute()
    if action == "View Other Critter Types":
        available_critters(user_date_obj)
    elif action == "Search":
        search()
    else:
        return

def print_available_critters(user_date, user_hemisphere, data):
    """Displays critters available today"""
    for critter_name, critter_data in data.items():
        if (
                user_date.month in critter_data["availability"][f"month-array-{user_hemisphere}"]
                and user_date.hour in critter_data["availability"]["time-array"]
        ):
            critter_name_en = critter_data["name"]["name-USen"]
            critter_time = critter_data["availability"]["time"]
            if critter_time == "":
                critter_time = "all day"
            with indent(4):
                puts(colored.green(f"{critter_name_en}, {critter_time}"))

def search():
    """Search and print critter information"""
    search_term = inquirer.text(message="Input critter name:").execute()

    # Blank search entry returns user to home page
    if search_term == "":
        return

    # Search in json files by critter name
    found_critter = search_critter("bugs", search_term) or \
                    search_critter("fish", search_term) or \
                    search_critter("sea", search_term)

    if not found_critter:
        with indent(4):
            puts(colored.red("Critter not found"))

    # Prompt user if they want to search again
    action = inquirer.select(
        message="Would you like to search again?",
        choices=[
            "Yes",
            Choice(value=None, name="← BACK"),
        ],
        default="Yes"
    ).execute()
    if action == "Yes":
        search()
    else:
        return

def search_critter(category, search_term):
    """Search for critter in JSON files by category and user's search term. Return True, if critter found."""
    with open(f"json/{category}.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for critter_name, critter_data in data.items():
            critter_name_en = critter_data["name"]["name-USen"]
            if search_term.lower() == critter_name_en.lower():
                critter_time = critter_data["availability"]["time"]
                if critter_time == "":
                    critter_time = "all day"
                with indent(4):
                    puts(colored.green(f"{critter_name_en} ({category})"))
                    puts(colored.green(f"{critter_time}"))
                if category == "bugs" or category == "fish":
                    with indent(4):
                        puts(colored.green(f"Location: {critter_data['availability']['location']}"))
                        puts(colored.green(f"Rarity: {critter_data['availability']['rarity']}"))
                elif category == "sea":
                    with indent(4):
                        puts(colored.green(f"Speed: {critter_data['speed']}"))
                        puts(colored.green(f"Shadow Size: {critter_data['shadow']}"))
                with indent(4):
                    puts(colored.green(f"Sell Price: {critter_data['price']} Bells"))
                return True

def change_date_hemisphere(user_date_obj):
    """Prompts user to change date and hemisphere"""
    current_month = calendar.month_name[user_date_obj.date.month]
    current_day = str(user_date_obj.date.day)
    current_year = str(user_date_obj.date.year)

    # Prompt user for new month
    new_month = inquirer.select(
        message="Select a month:",
        choices=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
            Choice(value=None, name="← BACK")
        ],
        default=current_month,
    ).execute()

    if new_month is None:
        return

    # Prompt user for hemisphere
    new_hemisphere = inquirer.select(
        message="Select a hemisphere:",
        choices=["Northern", "Southern"],
        default=user_date_obj.hemisphere.capitalize(),
    ).execute()

    # Update date and hemisphere
    new_date = datetime.strptime(f"{new_month} {current_day} {current_year}", "%B %d %Y")
    user_date_obj.change_date(new_date)
    user_date_obj.change_hemisphere(new_hemisphere)

def about():
    """Displays an about page for additonal information and instructions"""
    with indent(4):
        puts(colored.yellow("What is this Animal Crossing Critterpedia Library?"))
    with indent(8):
        puts("Animal Crossing New Horizon is game made by Nintendo. In the game there are three types of critters")
        puts("which the player can catch: bugs, fish, and sea creatures. The availability of any individual critter")
        puts("depends on the date, time, and hemisphere in real life. This library allows users to check the")
        puts("availability of critters on the current day.")
    with indent(4):
        puts(colored.yellow("How to Use:"))
    with indent(8):
        puts("Use `arrow keys` and `enter` for navigating between options.")
        puts(colored.yellow("Today's Critters:") + " Displays the current critters available today.")
        puts(colored.yellow("Search:") + " Input the critter name and press `enter`.")
        puts("This let's you view further information on the location/rarity/speed/price/etc of a critter.")
        puts("The search function is somewhat case sensitive, so make sure that you include spaces and punctuation.")
        puts(colored.yellow("Change Date & Hemisphere:") + " Configures the hemisphere or date to a different month.")
        puts("This alters the critters that are displayed on `Today's Critters`.")
        puts(colored.yellow("Generate Random") + "Let's you simulate catching a critter, like in Animal Crossing")
        puts("Note that there is a chance that you will be returned nothing.")

    inquirer.select(
        message="Press `enter` to return to homepage",
        choices=[
            Choice(value=None, name="← BACK"),
        ],
        default="← BACK"
    ).execute()

def home_nav():
    """Homepage"""
    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Today's Critters",
            "Search",
            "Change Date & Hemisphere",
            "Generate Random",
            "About",
            Choice(value=None, name="- EXIT"),
        ],
        default="Generate Name",
    ).execute()
    return action

def main():
    user_date_obj = Date(datetime.now(), "northern")
    puts(colored.yellow("Welcome to Animal Crossing Critter Library"))
    puts(colored.yellow("This library displays the available critters in the game Animal Crossing New Horizon."))
    puts(colored.yellow("Visit about page for more info about the game and this library."))
    puts(colored.yellow("use `arrow keys` and `enter` for navigating between options"))
    user_date_obj.display_date()
    user_date_obj.display_hemisphere()
    puts("-----------------------------------------------------------------------------------------------------------")
    while True:
        action = home_nav()
        if action == "Today's Critters":
            available_critters(user_date_obj)
        elif action == "Search":
            search()
        elif action == "Change Date & Hemisphere":
            change_date_hemisphere(user_date_obj)
        elif action == "Generate Random":
            generate()
        elif action == "About":
            about()
        else:
            break

if __name__ == "__main__":
    main()
