def list_maker_with_while_loop(max, step):
    i = 0
    list = []
    while i < max:
        list.append(i)
        i = i + step
    return list

def list_maker_with_for_loop(max, step):
    list = []
    for i in range(0, max, step):
        list.append(i)
    return list

def list_maker_with_just_range(max, step):
    return range(0, max, step)
