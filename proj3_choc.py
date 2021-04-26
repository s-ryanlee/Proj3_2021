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

def parse_command(command):
    """
    Parses a command string into a dictionary of query clause inputs.
    If the command string is missing parts of the query clause,
    default values are used instead.

    defaults:
    "hlc": 'bars',
    "select":"b.SpecificBeanBarName, b.Company, c.EnglishName, b.Rating, b.CocoaPercent, c.Region",
    "join":'CompanyLocationId',
    "where_type":None,
    "where_filter":None,
    "sort":'b.Rating',
    "direction":'desc',
    "limit":10

    PARAMETERS: command (str)
    -------------------------
    example: "bars sell region=Europe cocoa bottom 5"

    Returns: query_attribs (dict)
    -----------------------------
    A dictionary containing query clause input values.
    """

    hlc_options = ['bars', 'companies', 'countries', 'regions']
    join_options = ['sell', 'source']
    where_type_options = ['country', 'region']
    sort_options = ['ratings', 'cocoa', 'number_of_bars']
    direction_options = ['top', 'bottom']
    query_attribs = {"hlc": 'bars',
                "select":"b.SpecificBeanBarName, b.Company, c.EnglishName, b.Rating, b.CocoaPercent, c.Region",
                "join":'CompanyLocationId',
                "where_type":None,
                "where_filter":None,
                "sort":'b.Rating',
                "direction":'desc',
                "limit":10}

    query_input_list = command.split(' ')

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
                query_attribs['sort'] = 'AVG(b.CocoaPercent)'
            elif item == 'number_of_bars':
                query_attribs['sort'] = 'COUNT(b.SpecificBeanBarName)'
            else:
                query_attribs['sort'] = 'AVG(b.Rating)'
        elif item in direction_options:
            if item == 'bottom':
                direction = 'asc'
                query_attribs['direction'] = direction
            else:
                direction = 'desc'
                query_attribs['direction'] = direction
        else:
            try:
                query_attribs['limit'] = int(item)
            except ValueError:
                pass

    if hlc == 'regions':
        select = f"c.Region, {query_attribs['sort']}"
    elif hlc == 'companies':
        select = f"b.Company, c.EnglishName, {query_attribs['sort']}"
    elif hlc == 'countries':
        select = f"c.EnglishName, c.Region, {query_attribs['sort']}"
    else:
        if query_attribs['sort'] == 'AVG(b.CocoaPercent)':
            query_attribs['sort'] = 'b.CocoaPercent'
            select = f"b.SpecificBeanBarName, b.Company, c.EnglishName, b.Rating, {query_attribs['sort']}, c.Region"
        elif query_attribs['sort'] == 'COUNT(b.SpecificBeanBarName)':
            query_attribs['sort'] = 'b.SpecificBeanBarName'
            select = f"{query_attribs['sort']}, b.Company, c.EnglishName, b.Rating, b.CocoaPercent, c.Region"
        else:
            query_attribs['sort'] = 'b.Rating'
            select = f"b.SpecificBeanBarName, b.Company, c.EnglishName, {query_attribs['sort']}, b.CocoaPercent, c.Region"
    query_attribs['select'] = select

    return query_attribs


def generate_query(query_attribs):
    """
    Generates a query string from different query clause inputs.

    Parameters: query_attribs (dict)
    -------------------------
    defaults:
    "hlc": 'bars',
    "select":"b.SpecificBeanBarName, b.Company, c.EnglishName, b.Rating, b.CocoaPercent, c.Region",
    "join":'CompanyLocationId',
    "where_type":None,
    "where_filter":None,
    "sort":'b.Rating',
    "direction":'desc',
    "limit":10

    Returns: query (str)
    -----------------------------
    A formatted query string.
    """
    if query_attribs['where_type'] is not None:
        if query_attribs['hlc'] == 'countries' or query_attribs['hlc'] == 'companies':
            query = (
                    f"Select {query_attribs['select']} from Bars b"
                    f" join Countries c on c.id=b.{query_attribs['join']}"
                    f" where {query_attribs['where_type']} like '{query_attribs['where_filter']}'"
                    "group by b.Company having count(SpecificBeanBarName) > 4"
                    f" order by {query_attribs['sort']} {query_attribs['direction']}"
                    f" limit {query_attribs['limit']};"
                )
        elif query_attribs['hlc'] == 'regions':
            query = (
                    f"Select {query_attribs['select']} from Bars b"
                    f" join Countries c on c.id=b.{query_attribs['join']}"
                    f" where {query_attribs['where_type']} like '{query_attribs['where_filter']}'"
                    "group by c.Region having count(SpecificBeanBarName) > 4"
                    f" order by {query_attribs['sort']} {query_attribs['direction']}"
                    f" limit {query_attribs['limit']};"
                )
    elif query_attribs['where_type'] is None:
        query = (
            f"Select {query_attribs['select']} from Bars b"
            f" join Countries c on c.id=b.{query_attribs['join']}"
            f" order by {query_attribs['sort']} {query_attribs['direction']}"
            f" limit {query_attribs['limit']};"
        )
    else:
        print('invalid query')
    return query


# Part 1: Implement logic to process user commands
def process_command(command):
    if command != 'exit':
        parsed_command = parse_command(command)
        query = generate_query(parsed_command)
        results = cur.execute(query).fetchall()
    else:
        print('...')
    return results


def load_help_text():
    with open('Proj3Help.txt') as f:
        return f.read()


# Part 2 & 3: Implement interactive prompt and plotting. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    valid_responses = ['bars', 'companies', 'countries', 'regions', 'help', 'exit']
    while True:
        response = input('Enter a command: ')
        if response == '':
            response = 'bars'
        command = response.split(' ')
        if command[0] in valid_responses:
            if command[0] == 'help':
                print(help_text)
                continue
            elif command[0] == 'exit':
                print('Closing...')
                break
            else:
                results = process_command(response)
                print(results)
        else:
            print('Enter a valid command. Type "help" to view documentation.')
            continue


# Make sure nothing runs or prints out when this file is run as a module/library
if __name__=="__main__":
    # TESTING PARSE COMMAND AND GENERATE QUERY
    # example_bars_command = 'bars sell region=Europe cocoa bottom 5'
    # print(example_bars_command)
    # print('------------------------------')
    # example_query_input_dict = parse_command(example_bars_command)
    # print(example_query_input_dict)
    # print('------------------------------')
    # example_query = generate_query(example_query_input_dict)

    interactive_prompt()



