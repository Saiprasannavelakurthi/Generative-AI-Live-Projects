import json

def load_design_rules():

    with open("templates/design_rules.json","r") as file:

        rules = json.load(file)

    return rules