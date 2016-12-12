def is_matched(expression):
    stack = []
    for item in expression:
        if len(stack) == 0:
            stack.append(item)
        else:
            if item == '{' or item == '[' or item == '(':
                stack.append(item)
            elif item == '}' and stack.pop() != '{':
                return False
            elif item == ']' and stack.pop() != '[':
                return False
            elif item == ')' and stack.pop() != '(':
                return False
    if len(stack) == 0:
        return True
    else:
        return False

t = int(input().strip())
for a0 in range(t):
    expression = input().strip()
    if is_matched(expression) == True:
        print("YES")
    else:
        print("NO")
