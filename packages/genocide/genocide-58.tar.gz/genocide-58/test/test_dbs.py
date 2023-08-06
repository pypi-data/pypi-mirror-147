# This file is placed in the Public Domain.


"database tests"


import inspect
import os
import random
import shutil
import sys
import unittest


from ocl import Class
from odb import Db, all, dump, find, fns, fntime, load, listfiles, hook, save
from oev import Event


Class.add(Event)


db = Db()
fn = "store/oev.Event/61cba0b9-29c7-4154-a6c4-10b7365b3730/2022-04-11/22:40:31.259218"


class Test_Dbs(unittest.TestCase):


    def setUp(self):
        e = Event()
        e.txt = "test"
        save(e)

    def tearDown(self):
        db.remove("oev.Event", {"txt": "test"})

    def test_Db(self):
        db = Db()
        self.assertTrue(type(db), Db)

    def test_Db_find(self):
        e = Event()
        e.txt = "test"
        save(e)
        res = db.find("oev.Event")
        self.assertTrue(res)

    def test_Db_findselect(self):
        res = db.find("oev.Event", {"txt": "test"})
        self.assertTrue(res)

    def test_Db_lastmatch(self):
        res = db.lastmatch("oev.Event")
        self.assertTrue(res)

    def test_Db_lasttype(self):
        res = db.lasttype("oev.Event")
        self.assertTrue(res)

    def test_Db_lastfn(self):
        res = db.lastfn("oev.Event")
        self.assertTrue(res)

    def test_Db_remove(self):
        e = Event()
        e.txt = "test"
        save(e)
        res = db.remove("oev.Event", {"txt": "test"})
        self.setUp()
        self.assertTrue(res)

    def test_types(self):
        res = db.types()
        self.assertTrue("oev.Event" in res)

    def test_wrongfilename(self):
        fn, _o = db.lastfn("oev.Event")
        shutil.copy(fn, fn + "bork")
        res = db.find("oev.Event")
        self.assertTrue(res)

    def test_wrongfilename2(self):
        fntime(fn+"bork")

    def test_fntime(self):
        t = fntime(fn)
        self.assertEqual(t,  1649709631.259218)

    def test_fns(self):
        fs = fns("oev.Event")
        self.assertTrue(fs)

    def test_hook(self):
        e = Event()
        e.txt = "test"
        p = save(e)
        o = hook(p)
        print(o, p)
        self.assertTrue("oev.Event" in str(type(o)) and o.txt == "test")

    def test_listfiles(self):
        fns = listfiles(".test")
        self.assertTrue(fns)
        
    def test_all(self):
        fns = all()
        self.assertTrue(fns)

    def test_dump(self):
        e = Event()
        e.txt = "test"
        p = dump(e, ".test/store/%s" % e.__stp__)
        o = Event()
        load(o, p)
        self.assertEqual(o.txt, "test")

    def test_find(self):
        objs = find("oev.Event", {"txt": "test"})
        self.assertTrue(objs)

                