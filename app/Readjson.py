import json


def json_dict():
    try:
        # Change filepath to be your path where bookkeeping.json is

        # filepath = r'C:\Users\jgran\Desktop\bookkeeping.json'
        # filepath = r'/Users/jerrygranillo/Desktop/bookkeeping.json'
        filepath = r'bookkeeping.json'
        with open(filepath, 'r') as json_data:
            d = json.load(json_data)
    except IOError as e:
        print "Error while reading json: " + e.message
    return d
