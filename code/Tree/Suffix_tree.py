
from pprint import pprint
from functools import reduce


def make_stree(word):
    """
    Returns a sufix tree represented as hash table
    """
    hash_tree = {}
    prev_letter = hash_tree
    for letter in word:
        node = {}
        prev_letter[letter] = node
        if letter not in hash_tree:
            hash_tree[letter] = node
        prev_letter = node
    return hash_tree


def merge_tree(left, right):
    r_tree = {}
    for w, branches in left.items():
        if w in right:
            r_tree[w] = merge_tree(branches, right[w])
        else:
            r_tree[w] = branches
    for w, branches in [(k, v) for k, v in right.items() if k not in left]:
        r_tree[w] = branches
    return r_tree


def is_sufix(sufix, tree):
    w, *tail = sufix
    if w not in tree:
        return False
    if not tail:
        return True
    return is_sufix(sufix[1:], tree[w])


def match(wtree, stree):
    """
    returns [groups]
    """
    groups = []
    for w, nodes in wtree.items():
        if w in stree:
            groups.append(w)
            for tail in match(nodes, stree[w]):
                groups.append(w + tail)
    return groups


def build_index(text):
    strees = map(make_stree, text)
    return reduce(merge_tree, strees, {})


tree = make_stree('abcda')
bar = make_stree('bar')
baz = make_stree('bazwerwetwet')
barr = make_stree('barr')

pprint(match(bar, baz))
