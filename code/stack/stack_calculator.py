stack = []

def get_numbers():
    stack.pop()
    b = int(stack.pop())
    a = int(stack.pop())
    return (a, b)

while True:
    val = input()
    stack.append(val)

    if val == "+":
        a, b = get_numbers()
        ans = a+b
        print(a, "+", b, "=", ans)
        stack.append(ans)
    elif val == "-":
        a, b = get_numbers()
        ans = a-b
        print(a, "-", b, "=", ans)
        stack.append(ans)
    elif val == "*":
        a, b = get_numbers()
        ans = a*b
        print(a, "*", b, "=", ans)
        stack.append(ans)
    elif val == "/":
        a, b = get_numbers()
        ans = a/b
        print(a, "/", b, "=", ans)
        stack.append(ans)
    elif val == "^":
        a, b = get_numbers()
        ans = a**b
        print(a, "^", b, "=", ans)
        stack.append(ans)
