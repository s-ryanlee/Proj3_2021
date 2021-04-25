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

# Part 1: Implement logic to process user commands
def process_command(command):
    default_highlvl = 'bars'
    if command.lower() == default_highlvl:
        results = cur.execute(default_query).fetchall()
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
    #interactive_prompt()

    # template for each high level command
    # clauses: select, where, sort, order, limit
    default_params = {
        'join': 'CompanyLocationId',
        'where': None,
        'sort': 'b.Rating',
        'direction': 'desc',
        'limit': 10
        }

    default_select = """b.SpecificBeanBarName,
                    b.Company,
                    c.EnglishName,
                    b.Rating,
                    b.CocoaPercent,
                    c.Region""" # CompanyLocation and BroadBeanOrigin are FK on Countries Table

    default_query = (
        f"Select {default_select} from Bars b"
        f" join Countries c on c.id=b.{default_params['join']}"
        f" order by {default_params['sort']} {default_params['direction']}"
        f" limit {default_params['limit']};"
        )

    default_command = 'bars'
    default_results = process_command(default_command)
    for result in default_results:
        print(result)

    #bars_query_filter = (f"Select {default_select} from Bars b"
    #                    f" join on Country c.id=b.{join}"
    #                    f" where {where} like {parm_input}"
    #                    f" order by {sort} {direction}"
    #                    f" limit {limit};")
    #example_bars_command = 'bars sell region=Europe cocoa bottom 5'

    #bars_example_params = example_bars_command.split(' ')
    #print(params)

    #companies_default_params = {}
    #companies_select = f'b.Company, c.EnglishName, AVG({parameter}) as avg {parameter}' # avg(rating, cocoa, or number of bars)

    #countries_default_params = {}
    #countries_select = f'c.Country, c.Region, AVG(b.{parameter}) as avg {parameter}' # avg(rating, cocoa, or number of bars)


    #regions_default_params = {}
    #regions_select = f'c.Region, AVG(b.{parameter})' # avg(rating, cocoa, or number of bars)

