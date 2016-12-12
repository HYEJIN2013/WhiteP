def walk_level(path, level=1):
    """Like os.walk, but takes `level` kwarg that indicates how deep the recursion will go.
    Notes:
      TODO: refactor `level`->`depth`
    References:
      http://stackoverflow.com/a/234329/623735
    Args:
      path (str):  Root path to begin file tree traversal (walk)
      level (int, optional): Depth of file tree to halt recursion at. 
        None = full recursion to as deep as it goes
        0 = nonrecursive, just provide a list of files at the root level of the tree
        1 = one level of depth deeper in the tree
    Examples:
      >>> root = os.path.dirname(__file__)
      >>> all((os.path.join(base,d).count('/')==(root.count('/')+1)) for (base, dirs, files) in walk_level(root, level=0) for d in dirs)
      True
    """
    if isinstance(level, NoneType):
        level = float('inf')
    path = path.rstrip(os.path.sep)
    if os.path.isdir(path):
        root_level = path.count(os.path.sep)
        for root, dirs, files in os.walk(path):
            yield root, dirs, files
            if root.count(os.path.sep) >= root_level + level:
                del dirs[:]
    elif os.path.isfile(path):
        yield os.path.dirname(path), [], [os.path.basename(path)]
    else:
        raise RuntimeError("Can't find a valid folder or file for path {0}".format(repr(path)))

def find_files(path, ext='', level=None, verbosity=0):
    """Recursively find all files in the indicated directory with the indicated file name extension
    Args:
      path (str):
      ext (str):   File name extension. Only file paths that ".endswith()" this string will be returned
      level (int, optional): Depth of file tree to halt recursion at. 
        None = full recursion to as deep as it goes
        0 = nonrecursive, just provide a list of files at the root level of the tree
        1 = one level of depth deeper in the tree
    Returns: 
      list of dicts: dict keys are { 'path', 'name', 'bytes', 'created', 'modified', 'accessed', 'permissions' }
        path (str): Full, absolute paths to file beneath the indicated directory and ending with `ext`
        name (str): File name only (everythin after the last slash in the path)
        size (int): File size in bytes
        created (datetime): File creation timestamp from file system
        modified (datetime): File modification timestamp from file system
        accessed (datetime): File access timestamp from file system
        permissions (int): File permissions bytes as a chown-style integer with a maximum of 4 digits 
          e.g.: 777 or 1755
    Examples:
      >>> sorted(d['name'] for d in find_files(os.path.dirname(__file__), ext='.py', level=0))[0]
      '__init__.py'
    """
    path = path or './'
    files_in_queue = []
    if verbosity:
        print 'Preprocessing files to estimate pb.ETA'
    # if verbosity:
    #     widgets = [pb.Counter(), '/%d bytes for all files: ' % file_bytes, pb.Percentage(), ' ', pb.RotatingMarker(), ' ', pb.Bar(),' ', pb.ETA()]
    #     i, pbar = 0, pb.ProgressBar(widgets=widgets, maxval=file_bytes)
    #     print pbar
    #     pbar.start()
    for dir_path, dir_names, filenames in walk_level(path, level=level):
        for fn in filenames:
            if ext and not fn.lower().endswith(ext):
                continue
            files_in_queue += [{'name': fn, 'path': os.path.join(dir_path, fn)}]
            files_in_queue[-1]['size'] = os.path.getsize(files_in_queue[-1]['path'])
            files_in_queue[-1]['accessed'] = datetime.datetime.fromtimestamp(os.path.getatime(files_in_queue[-1]['path']))
            files_in_queue[-1]['modified'] = datetime.datetime.fromtimestamp(os.path.getmtime(files_in_queue[-1]['path']))
            files_in_queue[-1]['created'] = datetime.datetime.fromtimestamp(os.path.getctime(files_in_queue[-1]['path']))
            # file_bytes += files_in_queue[-1]['size']
    if verbosity > 1:
        print files_in_queue
    return files_in_queue

def flatten_csv(path='.', ext='csv', date_parser=parse_date, verbosity=0, output_ext=None):
    """Load all CSV files in the given path, write .flat.csv files, return `DataFrame`s
    Arguments:
      path (str): file or folder to retrieve CSV files and `pandas.DataFrame`s from
      ext (str): file name extension (to filter files by)
      date_parser (function): if the MultiIndex can be interpretted as a datetime, this parser will be used
    Returns:
      dict of DataFrame: { file_path: flattened_data_frame }
    """
    date_parser = date_parser or (lambda x: x)
    dotted_ext, dotted_output_ext = None, None
    if ext != None and output_ext != None:
        dotted_ext = ('' if ext.startswith('.') else '.') + ext
        dotted_output_ext = ('' if output_ext.startswith('.') else '.') + output_ext
    table = {}
    for file_properties in find_files(path, ext=ext or '', verbosity=verbosity):
        file_path = file_properties['path']
        if output_ext and (dotted_output_ext + '.') in file_path:
            continue
        df = pd.DataFrame.from_csv(file_path, parse_dates=False)
        df = flatten_dataframe(df)
        if dotted_ext != None and dotted_output_ext != None:
            df.to_csv(file_path[:-len(dotted_ext)] + dotted_output_ext + dotted_ext)
        table[file_path] = df
    return table
