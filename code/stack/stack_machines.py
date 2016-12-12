
import operator


def stack_operations(stack, operands):
    assert len(stack) == len(operands) + 1

    def binary_operation(fn):
        a = stack.pop()
        b = stack.pop()
        stack.append(fn(a, b))

    print stack
    while operands:
        binary_operation(operands.pop())
        print stack

# 3 5 2 2 + * -
print "3 5 2 2 + * -"

s1 = [3, 5, 2, 2]
o1 = [operator.sub, operator.mul, operator.add]
stack_operations(s1, o1)

# 3 5 2 4 + * -
print "3 5 2 4 + * -"

s2 = [3, 5, 2, 4]
o2 = [operator.sub, operator.mul, operator.add]
stack_operations(s2, o2)
