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

class Query():
    def __init__(self, high_level_command='bars', select=bars_select, join='CompanyLocationId', where_type=None, where_filter=None, sort='AVG(b.Rating)', direction='desc', limit=10):
        self.command = high_level_command
        self.select = select
        self.join = join
        self.where_type = where_type
        self.where_filter = where_filter
        self.sort = sort
        self.direction = direction
        self.limit = limit

    def query_default_results(self):
        default_query = (
        f"Select {self.select} from Bars b"
        f" join Countries c on c.id=b.{self.join}"
        f" order by {self.sort} {self.direction}"
        f" limit {self.limit};"
        )
        results = cur.execute(default_query).fetchall()
        return results

    def query_filtered_results(self):
        if self.where_type is not None and self.where_filter is not None:
            country_filtered_query = (
                    f"Select {self.select} from Bars b"
                    f" join Countries c on c.id=b.{self.join}"
                    f" where {where_type} like '{where_filter}'"
                    f" order by {self.sort} {self.direction}"
                    f" limit {self.limit};"
                )
            results = cur.execute(country_filtered_query).fetchall()
        else:
            query_default_results(self)
            results = cur.execute(query_default_results(self)).fetchall()

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


def parse_command(command):
    hlc_options = ['bars', 'companies', 'countries', 'regions']
    join_options = ['sell', 'source']
    where_type_options = ['country', 'region']
    sort_options = ['ratings', 'cocoa', 'number_of_bars']
    direction_options = ['top', 'bottom']
    query_input_list = command.split(' ')

    if len(command) == 6:
        if query_input_list[0] in hlc_options:
            hlc = query_input_list[0]
            select = hlc + '_select'
        else:
            print("enter a valid high level command")

        if query_input_list[1] in join_options:
            if query_input_list[1] == 'source':
                join = "BroadBeanOriginId"
            else:
                join = 'CompanyLocationId'
        else:
            print("enter a valid join parameter")

        if '=' in query_input_list[2]:
            where = query_input_list[2].split()
            where_type = where[0]
            where_filter = where[1]
            if where_type == 'country':
                where_type = 'c.Alpha2'
            elif where_type == 'region':
                where_type = 'c.Region'
        else:
            where_type = None
            where_filter = None
            print("No where parameter")

        if query_input_list[3] in sort_options:
            if query_input_list[3] == 'cocoa':
                sort = 'AVG(b.CocoaPercent)'
            elif query_input_list[3] == 'number_of_bars':
                sort = 'COUNT(b.SpecificBeanBarName)'
            else:
                sort = 'AVG(b.Rating)'
        else:
            print("enter a valid sort parameter")

        if query_input_list[4] in direction_options:
            if query_input_list[4] == 'bottom':
                direction = 'asc'
            else:
                direction = 'desc'
        else:
            print("enter a valid direction paramter")

        if query_input_list[5] is int:
            limit = query_input_list[5]
        else:
            print("enter a valid limit parameter")
    else:
        print('enter a valid command')

        query_attribs = {'hlc': hlc,
                        'select': select,
                        'join': join,
                        'where_type': where_type,
                        'where_filter': where_filter,
                        'sort': sort,
                        'direction': direction,
                        'limit': limit}
    return query_attribs


def create_Query_instance(query_attribs):
    command_instance = Query(
        high_level_command=query_attribs['hlc'],
        select=query_attribs['select'],
        join=query_attribs['join'],
        where_type=query_attribs['where_type'],
        where_filter=query_attribs['where_filter'],
        sort=query_attribs['sort'],
        direction=query_attribs['direction'],
        limit=query_attribs['limit']
    )
    return command_instance


# Make sure nothing runs or prints out when this file is run as a module/library
if __name__=="__main__":
    default = Query()

    companies_select = f'b.Company, c.EnglishName, {default.sort}'
    countries_select = f'c.EnglishName, c.Region, {default.sort}'
    regions_select = f'c.Region, {default.sort}'

    companies_default = Query(high_level_command='companies', select=companies_select)
    countries_default = Query(high_level_command='countries', select=countries_select)
    regions_default = Query(high_level_command='regions', select=regions_select)

    default_results = default.query_default_results()
    default_companies_results = companies_default.query_default_results()
    default_countries_results = countries_default.query_default_results()
    default_regions_results = regions_default.query_default_results()

    example_bars_command = 'bars sell region=Europe cocoa bottom 5'
    example_query_input_list = parse_command(example_bars_command)
    print(query_input_list)





    #interactive_prompt()



