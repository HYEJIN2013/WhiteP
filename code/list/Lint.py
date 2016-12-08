from collections import defaultdict
class Lint(defaultdict):
  def __init__(self, item):
    super(Lint, self).__init__(int)
    if isinstance(item, int) or isinstance(item, long):
      st = str(item)[::-1]
      d = {i: int(st[i]) for i in xrange(len(st))}
    elif isinstance(item, dict):
      d = item
    else:
      return NotImplemented
    self.update(d)
    self.__clean()

  def __clean(self):
    for i in xrange(self.__len__()):
      val = self.__getitem__(i)
      if val >= 10:
        st = str(val)[::-1]
        self.__setitem__(i, int(st[0]))
        for j in xrange(1, len(st)):
          self.__setitem__(i+j, self.__getitem__(i+j) + int(st[j]))

  def __add__(self, other):
    if isinstance(other, int):
      other = Lint(other)
    if not isinstance(other, Lint):
      return NotImplemented
    result = defaultdict(int)
    maxlen = max(self.__len__(), len(other))
    for i in xrange(maxlen):
      result[i] = self.__getitem__(i) + other[i]
    return Lint(result)
