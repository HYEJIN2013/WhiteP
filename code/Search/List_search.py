def search_list(term, words, deep):
  result = []
  idx = 0
  while idx < len(words):
    try:
      idx = words.index(term, idx)
      result.append(idx)
      idx += 1  # Start from the next element
      if not deep:
        break
    except ValueError:
      break
  return result

def single_term_search(term, words, deep_search):
    """Gather index locations of a single word search within list of words.
    For efficiency, will stop and return only first instance if not deep_search
    Args:
        term (str): single word to search
        words (list): list of words in file in which to search
        deep_search (bool): iterate through entire list if True
    Returns:
        indexes (list): list of indexes where search term is found
    """

    indexes = list()
    for index, word in enumerate(words):
        if word == term:
            indexes.append(index)
            if not deep_search:
                break
    return indexes

if __name__ == '__main__':
    terms = ['foo', 'bar', 'baz'] * 10000000
    search_list('foo', terms, True)
    #single_term_search('foo', terms, True)
