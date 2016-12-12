import sys

def suffix_tree(chunk_strip,n):
    """ 
    generate a dictionary representation of a suffix tree
    """
    if len(chunk_strip) % n != 0: print "Try different n-gram" ,sys.exit(1)    
    suffix_tree = dict()
    for stop, start in enumerate(range(0,len(chunk_strip), n)):
        
        stop  = (stop + 1)*n
        curr =  chunk_strip[start:]
        suffix_tree.update({start:curr})
    
    return suffix_tree   
        
