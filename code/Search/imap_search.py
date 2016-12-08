import getpass, imaplib
from itertools import islice
from email.parser import HeaderParser

def number_set(seq):
    res = []
    last = first = next(seq)
    for i in seq:
        assert last < i
        if i - last == 1:
            last = i
        else:
            if last == first:
                res.append(str(last))
            else:
                res.append("{0:d}:{1:d}".format(first,last))
            first = last = i
    if last == first:
        res.append(str(last))
    else:
        res.append("{0:d}:{1:d}".format(first,last))
    return ','.join(res)


def search(*criteria):
    connection = imaplib.IMAP4_SSL("imap.gmail.com")
    user = input('User name: ')
    pswd = getpass.getpass()
    connection.login(user, pswd)    
    connection.select()
    typ, search_data = connection.uid('SEARCH', None, *criteria)
    for search_batch in search_data:
        message_set = number_set(int(i) for i in search_batch.split())
        typ, fetch_data = connection.uid("FETCH", message_set, '(BODY[HEADER.FIELDS (DATE FROM SUBJECT)])')
        for msg in islice(fetch_data, 0, None, 2):
            yield msg[1]
    connection.close()
    connection.logout()
    

parser = HeaderParser()
for raw_headers in search('FROM','john'):
    print(parser.parsestr(raw_headers))
