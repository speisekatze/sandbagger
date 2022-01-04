# -*- coding: utf-8 -*-
"""
Aggregator normalizing Blocklists and merge them
Created on Fr Mar 06 18:30:29 2020

@author: n4p
"""


def normalize(data, fmt):
    """ remove lines starting with # and replace whatever ip is in one line with 0.0.0.0 """
    normalized = []
    for item in data:
        line = item.decode("utf-8").split()
        if len(line) < 1 or line[0][0] == "#":
            continue
        s = "0.0.0.0 "
        if fmt == 1:
            s = ""
        normalized.append(s + line[1])
    return normalized


def merge(blacklists, dupes=False):
    """ merging multiple blacklists leaving or removing duplicates """
    newlist = []
    if len(blacklists) > 1:
        popped = blacklists.pop()
        list_a = popped["data"]
    else:
        popped = blacklists.pop()
        return popped["data"]

    list_b = merge(blacklists, dupes)

    if dupes:
        newlist = list_a + list_b
    else:
        list_diff = set(list_b) - set(list_a)
        newlist = list_a + list(list_diff)
    return newlist
