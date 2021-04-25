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
# CompanyLocation and BroadBeanOrigin are FK on Countries Table

class Query():
    def __init__(self, hlc='bars',
                select="b.SpecificBeanBarName, b.Company, c.EnglishName, b.Rating, b.CocoaPercent, c.Region",
                join='CompanyLocationId',
                where_type=None,
                where_filter=None,
                sort='b.Rating',
                direction='desc',
                limit=10):

        self.command = hlc
        self.select = select
        self.join = join
        self.where_type = where_type
        self.where_filter = where_filter
        self.sort = sort
        self.direction = direction
        self.limit = limit

    def print_attributes(self):
        return print(
            f"command: {self.command}\nselect: {self.select}\njoin: {self.join}\nwhere_type: {self.where_type}\nwhere_filter: {self.where_filter}\nsort: {self.sort}\ndirection: {self.direction}\nlimit: {self.limit}"
        )

    def print_query(self):
        if self.where_type is not None:
            filtered_query = (
                    f"Select {self.select} from Bars b"
                    f" join Countries c on c.id=b.{self.join}"
                    f" where {where_type} like '{where_filter}'"
                    f" order by {self.sort} {self.direction}"
                    f" limit {self.limit};"
                )
            print(filtered_query)
            #results = cur.execute(country_filtered_query).fetchall()
        elif self.where_type is None:
            default_query = (
                f"Select {self.select} from Bars b"
                f" join Countries c on c.id=b.{self.join}"
                f" order by {self.sort} {self.direction}"
                f" limit {self.limit};"
            )
            print(default_query)
            #results = cur.execute(default_query).fetchall()
        return None



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
    digits = ['0', '1', '2', '3', '4', '5', '6','7', '8','9']
    query_input_list = command.split(' ')
    query_attribs = {}

    for item in query_input_list:
        if item in hlc_options:
            hlc = item
            query_attribs['hlc'] = hlc
        elif item in join_options:
            if item == 'source':
                join = "BroadBeanOriginId"
                query_attribs['join'] = join
            else:
                join = 'CompanyLocationId'
                query_attribs['join'] = join
        elif '=' in item:
            where = item.split('=')
            where_type = where[0]
            where_filter = where[1]
            if where_type == 'country':
                where_type = 'c.Alpha2'
                query_attribs['where_type'] = where_type
                query_attribs['where_filter'] = where_filter
            elif where_type == 'region':
                where_type = 'c.Region'
                query_attribs['where_type'] = where_type
                query_attribs['where_filter'] = where_filter
        elif item in sort_options:
            if item == 'cocoa':
                sort = 'AVG(b.CocoaPercent)'
                #query_attribs['sort'] = sort
            elif item == 'number_of_bars':
                sort = 'COUNT(b.SpecificBeanBarName)'
                #query_attribs['sort'] = sort
            else:
                sort = 'AVG(b.Rating)'
                #query_attribs['sort'] = sort
        elif item in direction_options:
            if item == 'bottom':
                direction = 'asc'
                query_attribs['direction'] = direction
            else:
                direction = 'desc'
                query_attribs['direction'] = direction
        elif item in range(1,999):
            limit = int(item)
            query_attribs['limit'] = limit

    if hlc == 'regions':
        select = f'c.Region, {sort}'
    elif hlc == 'companies':
        select = f'b.Company, c.EnglishName, {sort}'
    elif hlc == 'countries':
        select = f'c.EnglishName, c.Region, {sort}'
    else:
        if sort == 'AVG(b.CocoaPercent)':
            sort = 'b.CocoaPercent'
            select = f"b.SpecificBeanBarName, b.Company, c.EnglishName, b.Rating, {sort}, c.Region"
        elif sort == 'COUNT(b.SpecificBeanBarName)':
            sort = 'b.SpecificBeanBarName'
            select = f"{sort}, b.Company, c.EnglishName, b.Rating, b.CocoaPercent, c.Region"
        else:
            sort = 'b.Rating'
            select = f"b.SpecificBeanBarName, b.Company, c.EnglishName, {sort}, b.CocoaPercent, c.Region"
    query_attribs['select'] = select
    query_attribs['sort'] = sort

    return query_attribs


def create_Query_instance(query_attribs):
    command_instance = Query(query_attribs)
    return command_instance


# Make sure nothing runs or prints out when this file is run as a module/library
if __name__=="__main__":
    example_bars_command = 'bars sell region=Europe cocoa bottom 5'
    print(example_bars_command)
    print('------------------------------')
    example_query_input_dict = parse_command(example_bars_command)
    print(example_query_input_dict)
    print('------------------------------')
    example_query_instance = create_Query_instance(example_query_input_dict)
    example_query_instance.print_attributes()
    example_query_instance.print_query()

    #interactive_prompt()



