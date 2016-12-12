from stack import Stack

stack1=Stack()
stack2=Stack()

def pandromeChecker(ifade):
    for ch in ifade:
        if "A"<=ch<="Z" or "a"<=ch<="z" or "16"<=ch<="25":
            stack1.push(ch)
    for letters in ifade:
        if "A"<=letters<="Z" or "a"<=letters<="z" or "16"<=ch<="25":
            stack2.push(letters)
            
        stack2.reverse()
        
def stack_equals(stack,stack2):
    while true:
        try:
            if stack1.pop() != stack2.pop():
                return false
        except IndexError:
                return true
