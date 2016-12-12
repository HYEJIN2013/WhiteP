import math

def recursive_tree(root, spacing=0, depth=1):
    print("{:3}: {} {}".format(depth, "-"*spacing, str(root)))
    if isinstance(root, tuple):
        for c in root:
            recursive_tree(c, spacing+4, depth+1)

# Preprocessing
padding = 16
sent = "A person on a horse jumps over a broken down airplane"

print("PADDING: {}".format(padding))
print("INITIAL SENTENCE: {}".format(sent))

sent = sent.split()
sent = ["EMPTY"] * (padding - len(sent)) + sent
depth = int(math.log(len(sent), 2)) + 1

print("PADDING SENTENCE: {}".format(" ".join(sent)))
print("TREE DEPTH: {}".format(depth))
print

# Initialize Tree Output
tree = [[] for i in range(2**depth-1)]
for ii, i in enumerate(reversed(range(len(sent)))):
    tree[len(tree) - ii - 1] = sent[i]

# Build Tree
for d in reversed(range(1, depth)):
    for s in range(2**d-1, 2**(d+1)-1, 2):
        tree[(s-1)/2] = (tree[s], tree[s+1])

# Read Tree
output = []
for d in reversed(range(1, depth)):
    for s in range(2**d-1, 2**(d+1)-1, 1):
        output.append(tree[s])

# Print Tree
print("TREE STATES:")
print("""
    These are the hidden states generated with the
    TreeLSTM function. The leaves are the words. This
    is an array representation of a binary tree:
    root=0, left_child=parent*2, right_child=parent*2+1
    """)
for ii, o in enumerate(tree):
    print("{:3}: {}".format(ii, o))
print

print("TREE STATES (pretty format for pre-order):")
recursive_tree(tree[0])
print

# Print Output
print("OUTPUT STATES (post-order traversal):")
for ii, o in enumerate(output):
    print("{:3}: {}".format(ii, o))
print
