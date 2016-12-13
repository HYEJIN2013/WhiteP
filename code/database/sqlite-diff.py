#!/usr/bin/python

import sys, sqlite3, tempfile, subprocess, os

def do_select(connection, table, fields):
    connection.row_factory = sqlite3.Row
    c = connection.cursor()

    # If no fields are given, use all fields
    if fields == []:
        fields = ['*']

    # Get all the fieldnames if * is provided
    if fields[0] == "*":
        c.execute("SELECT * FROM %s LIMIT 1"% (table))
        fields = c.fetchone().keys() + fields[1:]

    c.execute("SELECT %s FROM %s ORDER BY %s ASC"% (", ".join(fields), table, fields[0]))
    return c

def compare_db(c1, c2, table, fields):
    global diff
    global diff_options
    global dwdiff
    
    files = []
    for c in [c1, c2]:
        rows = do_select(c, table, fields)
        # Fill a Temporary file with the results of the SELECT statement
        f = tempfile.NamedTemporaryFile()
        for row in rows:
            row = [unicode(x).replace("\n", "\\n") for x in row]
            row = " || ".join(row) + "\n"
            f.write(row.encode("utf-8"))
        f.flush()
        files.append(f)

    # Call the diff programm on these two files
    a = subprocess.Popen(diff + diff_options + [f.name for f in files], stdout=subprocess.PIPE)
    for line in a.stdout.readlines():
        if line != "--\n" or not dwdiff:
            print line[:-1]

            

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "usage: %s <database1> <database2> <table> [field1] [field2] ... [fieldn] [ -- diff options ]" % sys.argv[0]
        sys.exit(1)

    if os.path.exists("/usr/bin/dwdiff"):
        dwdiff = True
        diff = ["dwdiff", "-c", "-C", "0"]
    else:
        diff = ["diff", "-u"]
        dwdiff = False

    try:
        del sys.argv[0]

        # Create database connection 1
        c1 = sqlite3.connect(sys.argv[0])
        del sys.argv[0]

        # Create database connection 2
        c2 = sqlite3.connect(sys.argv[0])
        del sys.argv[0]

        table = sys.argv[0]
        del sys.argv[0]

        # Collect all diff options after the --
        diff_options = []
        if "--" in sys.argv:
            i = sys.argv.index("--")
            diff_options = sys.argv[i+1:]
            sys.argv = sys.argv[:i]

        fields = sys.argv

        compare_db(c1, c2, table, fields)

    except:
        raise      
