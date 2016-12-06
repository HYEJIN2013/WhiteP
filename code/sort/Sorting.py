def sorting( an_array ):
    final = []
    count = 0
    an_array = sorted( an_array )
    total = len( an_array )
    while count < total:
        if count % 2 == 0:
            element = an_array[ 0 ]
            del an_array[ 0 ]
        else:
            element = an_array[ -1 ]
            del an_array[ -1 ]
        final.append( element )
        count = count + 1
    return final
