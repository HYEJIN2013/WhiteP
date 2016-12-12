class Stack:
  def __init__(self):
    self.stack = []

  def push(self, el):
    self.stack.append(el)

  def pop(self):
    if len(self.stack) == 0:
      raise StackEmptyError()

  def size(self):
    return len(self.stack)

  class StackEmptyError(Error):
    pass

stack = Stack()
