# Example final output:
#
# 1000 main
#   1000 workLoop
#     900 read
#       900 __sys_read
#     100 parse
#       100 strcmp
#

import doctest
from functools import reduce

# Implemented for you


def get_stacktraces():
    return [
        ["main", "workloop", "select"],
        ["main", "parse_args"],
        ["main", "workloop", "parse_data", "parse_entry"],
        ["main", "workloop", "select"]
    ]


def new_node(name, childs=None):
    return {'name': name, 'count': 0,
            'childs': {ch.name: ch for ch in childs or []}}


def add_child(node, child_name):
    """
    >>> main = new_node('main')
    >>> main
    {'count': 0, 'childs': {}, 'name': 'main'}
    >>> add_child(main, 'ImmaChild')
    {'count': 0, 'childs': {}, 'name': 'ImmaChild'}
    """
    child_node = new_node(child_name)
    node['childs'][child_name] = child_node
    return child_node


def pretty_print(tree, ident_level=0):
    print('{count} {name}\n {ident}'.format(
        ident='\t' * ident_level, **tree), end='')
    for ch in tree['childs'].values():
        pretty_print(ch, ident_level=ident_level + 1)


def build_tree(tree, trace):
    def buid(node, fns):
        if not fns:
            return tree
        first, *tail = fns
        if first == node['name']:
            tree['count'] += 1
            return buid(node, tail)
        else:
            child_node = node['childs'].get(first) or add_child(node, first)
            child_node['count'] += 1
            return buid(child_node, tail)
    return buid(tree, trace)


tree = reduce(build_tree, get_stacktraces(), new_node('main'))

pretty_print(tree)
doctest.testmod()
