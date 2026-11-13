def find_index(items, wanted):
    for i, item in enumerate(items):
        if item == wanted:
            return i
    return -1
