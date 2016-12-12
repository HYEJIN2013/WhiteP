# -*- coding: utf-8 -*- 
import distutils, sys, distutils.dir_util
 
def main():
    if len(sys.argv) is 3:
        distutils.dir_util.copy_tree(sys.argv[1], sys.argv[2])
    else:
        print('use: pycopy <from> <to>')
 
if __name__ == "__main__":
    main()
