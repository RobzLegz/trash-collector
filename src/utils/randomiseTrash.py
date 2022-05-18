import random

trash_options = [
    "Bottle.osgb",
    "GlassBottle.osgb",
]

def get_random_trash():
    trash_option_index = random.randint(0, (len(trash_options) - 1))

    trash_option = trash_options[trash_option_index]

    return trash_option