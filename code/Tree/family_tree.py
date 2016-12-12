from pprint import pprint

data = {
    "children": [
        {
            "id": 409,
            "name": "Joe Bloggs",
            "no_parent": "true"
        },
        {
            "children": [
                {
                    "children": [
                        {"id": 509,
                        "name": "x",},

                        {"id": 519,
                        "name": "y",},

                        ],
                    "id": 411,
                    "name": "Alice Bloggs"
                },
                {
                    "children": [],
                    "id": 412,
                    "name": "John Bloggs"
                }
            ],
            "hidden": "true",
            "id": "empty_node_id_9",
            "name": "",
            "no_parent": "true"
        },
        {
            "children": [],
            "id": 410,
            "name": "Sarah Smith",
            "no_parent": "true"
        }
    ],
    "hidden": "true",
    "id": "year0",
    "name": ""
}        

class Person(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.id = kwargs['id']
        self.hidden = kwargs['hidden']
        self.children = kwargs.get('children', [])

    def __repr__(self):
        return '(Person: {}, {})'.format(self.name, self.id)

def parse_dict(tree, root):
    '''helper function that handles dictionary leafs'''

    # first some error checking
    if not isinstance(tree, dict):
        raise Exception('parse dict called on non dict')
    if 'name' not in tree:
        raise Exception('Mystry dic: '.format(tree))

    # now add the new person
    person = Person(name = tree['name'],
                    id = tree['id'],
                    hidden = tree.get('hidden')
                    )
    # put him into your new tree structure
    if root is None:
        root = person
    else:
        root.children.append(person)

    # recursively check and add children
    if 'children' in tree:
        parse_tree(tree['children'], person)

    return root

def parse_list(tree, root):
    if not isinstance(tree, list):
        raise Exception('parse list called on non list')
    
    for item in tree:
        root = parse_tree(item, root)


    return root


def parse_tree(tree, root = None):
    if isinstance(tree, dict):
        root = parse_dict(tree, root)
    elif isinstance(tree, list):
        root = parse_list(tree, root)

    return root

def print_nodes(node, depth = 0):
    if not node:
        return
    depth += 1
    if node.hidden != 'true':
        spacing = ' '*(depth*5)
        print('{}{}'.format(spacing, node))
    for child in node.children:
        print_nodes(child, depth)
            
t = parse_tree(data)
print_nodes(t)
