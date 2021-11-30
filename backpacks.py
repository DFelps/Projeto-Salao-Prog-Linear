def generate_backpack(size, available_weight):
    
    backpack = {
        "available_weight": available_weight,
        "list_items": []
    }

    for i in range(size):
        backpack["list_items"].append(0)

    return backpack
