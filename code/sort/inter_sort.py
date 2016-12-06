#!/user/bin/python
# -*- coding: utf-8 -*-
import sys, logging

def inter_sort(lines):
    m = {}
    for i, line in enumerate(lines):
        l = line.strip()
        try:
            _,suffix = l.lower().split("@")
        except:
            logging.exception("invalid email:%s at line:%d", l, i)
        if not m.has_key(suffix):
            m[suffix] = []
        m[suffix].append(l)

    ret = []
    while True:
        if not m:
            break
        for k in m.keys():
            v = m[k]
            if v:
                ret.append(v[0])
                m[k] = v[1:]
            else:
                del m[k]
        ret.append('')
    return ret

if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("Usage: %s <file>" % sys.argv[0])
        exit(1)

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
        result = inter_sort(lines)
        for line in result:
            print(line)
