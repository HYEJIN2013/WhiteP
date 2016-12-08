r__ = 'Vinoth'

class SinglyLinkedLists:

  class _Node:

      __Slots__ = '_element', '_next'

      def __init__(self,element,next):
          self._element = element
          self._next = next

  def __init__(self):
      self._head = None
      self._size = 0

  def __len__(self):
      return self._size

  def is_empty(self):
      return self._size == 0

  def push(self,e):

      if self.is_empty():
          raise Empty ('Stack is Empty')
      return self._head._element

  def pop(self):

      if self.is_empty():
          raise Empty ('Stack is Empty')
      answer = self. head. element
      self._head = self. head. next
      self._size -= 1
      return answer
