# Samantha Ryan-Lee
# sryanlee

import sqlite3

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from a database called choc.db
DBNAME = 'choc.sqlite'
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()
bars_select = """b.SpecificBeanBarName,
                    b.Company,
                    c.EnglishName,
                    b.Rating,
                    b.CocoaPercent,
                    c.Region""" # CompanyLocation and BroadBeanOrigin are FK on Countries Table

class Default():
    def __init__(self, high_level_command='bars', select=bars_select):
        self.command = high_level_command
        self.select = select
        self.join = 'CompanyLocationId'
        self.where = None
        self.sort = 'b.Rating'
        self.direction = 'desc'
        self.limit = 10

    def get_default_results(self):
        default_query = (
        f"Select {self.select} from Bars b"
        f" join Countries c on c.id=b.{self.join}"
        f" order by {self.sort} {self.direction}"
        f" limit {self.limit};"
        )
        results = cur.execute(default_query).fetchall()
        return results


# Part 1: Implement logic to process user commands
def process_command(command):
    high_levels = ['bars', 'companies', 'countries', 'regions']
    if command.lower() == default.command:
        results = default.get_default_results()

    return results

def load_help_text():
    with open('help.txt') as f:
        return f.read()

# Part 2 & 3: Implement interactive prompt and plotting. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')

        if response == 'help':
            print(help_text)
            continue

# Make sure nothing runs or prints out when this file is run as a module/library
if __name__=="__main__":
    default = Default()
    #interactive_prompt()

    default_results = default.get_default_results()
    for result in default_results:
        print(result)

    # bars_query_filter = (f"Select {default_select} from Bars b"
    #                     f" join on Country c.id=b.{join}"
    #                     f" where {where} like {parm_input}"
    #                     f" order by {sort} {direction}"
    #                     f" limit {limit};")
    # example_bars_command = 'bars sell region=Europe cocoa bottom 5'


    #companies_default_params = {}
    #companies_select = f'b.Company, c.EnglishName, AVG({parameter}) as avg {parameter}' # avg(rating, cocoa, or number of bars)

    #countries_default_params = {}
    #countries_select = f'c.Country, c.Region, AVG(b.{parameter}) as avg {parameter}' # avg(rating, cocoa, or number of bars)


    #regions_default_params = {}
    #regions_select = f'c.Region, AVG(b.{parameter})' # avg(rating, cocoa, or number of bars)

