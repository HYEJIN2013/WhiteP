'''
 Fuzzy search algorithm inspired by sublimetext.
'''

with open('/usr/share/dict/words') as f:
    words = f.read().split('\n')

def fuzzy_match (q):
    ''' Match a query string q against a candidate string s, where len(q) <= len(s).
    Returns true iff q is a partially ordered subset of s, or false otherwise.
    ('sbl' is an ordered subset of 'sublime'; 'stbl' and 'slb' are not)
    '''
    def match (s):
        i, j = len(s), len(q)
        while j != 0 and i >= j:
            if s[i-1] == q[j-1]:
                j -= 1
            i -= 1
        return j == 0
    return match

def matching_words (q):
    return filter(fuzzy_match(q), words)

queries = [ 'abaion', 'cmkng', 'sblme' ]

for q in queries:
    print('%s: %s'%(q, '\n\t'.join(
        sorted(matching_words(q),key=len))))
