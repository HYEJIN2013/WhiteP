import traceback

def foo():
    x = [1, 2, 3]
    print(traceback.extract_stack())

if __name__ == '__main__':
    foo()
