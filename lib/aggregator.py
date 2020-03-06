import urllib.request as ur

def normalize(data):
    normalized = []
    for item in data:
        line = item.decode('utf-8').split()
        if len(line) < 1 or line[0][0] is '#':
            continue
        else:
            normalized.append('0.0.0.0 ' + line[1])
    return normalized

def merge(blacklists, bDupes=False):
    newlist = []
    if len(blacklists) > 1:
        popped = blacklists.pop()
        print(popped['name'])
        list_a = popped['data']
    else:
        popped = blacklists.pop()
        print(popped['name'])
        return popped['data']

    list_b = merge(blacklists,bDupes)

    if bDupes:
        newlist = list_a + list_b
    else:
        list_diff = set(list_b) - set(list_a)
        newlist = list_a + list(list_diff)
    return newlist
