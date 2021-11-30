from random import randint
from pprint import pprint

def item_weight_generator(backpack_weight):
    MAX_WEIGHT = int(backpack_weight * 0.60)
    MIN_WEIGHT = int(backpack_weight * 0.15)

    item_weight = randint(MIN_WEIGHT, MAX_WEIGHT)

    return item_weight


def generating_item(backpack_weight):
    item = item_weight_generator(backpack_weight)
 
    return item


def generating_list_item(number_of_items, backpack_weight):
    list_items = []

    for i in range(number_of_items):
        item = generating_item(backpack_weight)

        list_items.append(item)

    return list_items


def get_lighter_item(list_items):
    order = sorted(list_items)
    lighter_item = order[0]
    
    return lighter_item
