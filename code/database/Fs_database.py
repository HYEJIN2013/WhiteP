#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# NOT Thread-Safe!
# now support only text files

# TODO:
# 1. Remove self.path in functions

import os
import shutil
from datetime import datetime

class DB(object):
    path = "/home/bkmz/Dev/python/2gis-web/database"

    DATA = "/data"
    TYPE = "/type"
    JSON = "/json"
    LAST = "/last_update"

    def __init__(self):
        # current position in DB
        self.cursor = ""
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def set(self, path, data, type=DATA, rewrite=False):
        path = self._check_path(path)
        if (os.path.exists(self.path+path)) and rewrite:
            self._write(path, data, type)
        elif not os.path.exists(self.path+path):
            self._write(path, data, type)
        else:
            return -1

    def create_link(self, path_to, path_from):
        if os.path.exists(self.path + path_to):
            return -1

        if len(path_from.split("/")) == len(path_to.split("/")):
            os.symlink(self.path+path_from, self.path+path_to)
        else:
            raise AttributeError("Different levels for symlinks not allowed")


    def get(self, path, type=DATA):
        path = self._check_path(path)

        if (os.path.exists(self.path+path+type)):
            hl = open(self.path+path+type, "r")
            out = hl.read()
            hl.close()
            return out

    def get_last(self, path):
        return self.get(path, self.LAST)

    def exists(self, path, type=None):
        if type == None:
            for i in [self.DATA, self.TYPE, self.JSON, self.LAST]:
                if os.path.exists(self.path+path+i):
                    return True
        else:
            if os.path.exists(self.path+path+type):
                return True

        return False

    # NOT SAFE!!!
    def delete(self, path):
        # delete / is not allowed
        if path == "/":
            raise RuntimeError("delete is disabled now")

        raise RuntimeError("delete is disabled now")
        if not os.path.exists(self.path+path):
            return -1

        if os.path.islink(self.path+path):
            os.unlink(self.path+path)
        elif os.path.isdir(self.path+path):
            shutil.rmtree(self.path+path)

    def delete_db(self):
        shutil.rmtree(self.path)


    def _write(self, path, data, type):
        if not (os.path.exists(self.path+path)):
            os.makedirs(self.path+path)
        hl = open(self.path+path+type, "w")
        hl.write(data)
        hl.close()

        hl=open(self.path+path+self.LAST, "w")
        hl.write(datetime.now().__str__())
        hl.close()


    def _check_path(self, path):
        if path == None or len(path) == 0:
            raise AttributeError("Path is not set")

        elif not path[0] == "/":
            raise AttributeError("Path must begins with /")

        return path.lower()


if __name__ == "__main__":
    obj = DB()

    # obj.set('/1', "DATA")
    # obj.create_link("/moscow", "/1")

    # obj.delete("/moscow")
    # obj.delete("/1")


    obj.set("/" , "132342312", DB.JSON, rewrite=True)

