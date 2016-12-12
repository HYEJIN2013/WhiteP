# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import os
from os.path import join, abspath
import shutil


sourcedir = abspath(sys.argv[1])
out1 = abspath(sys.argv[2]) if len(sys.argv) >= 3 else 'out1'
out2 = abspath(sys.argv[3]) if len(sys.argv) >= 4 else 'out2'
outdirs = [out1, out2]


relpath = lambda path: path[len(sourcedir) + 1:]

# If out dir doesn't exist create it, if it does empty it.
for outdir in outdirs:
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    else:
        for file_object in os.listdir(outdir):
            file_object_path = join(outdir, file_object)
            if os.path.isfile(file_object_path):
                os.unlink(file_object_path)
            else:
                shutil.rmtree(file_object_path)

for root, dirs, files in os.walk(sourcedir):
    root_rel_path = relpath(root)
    if root != sourcedir:
        for outdir in outdirs:
            os.makedirs(join(outdir, root_rel_path))

    file_count = len(files)
    limit_idx = file_count * 0.75 - 1
    for i, filename in enumerate(files):
        outdir = outdirs[0 if i < limit_idx else 1]
        src = join(root, filename)
        dest = join(outdir, root_rel_path)
        print(src, ' -> ', dest)
        shutil.copy(src, dest)
