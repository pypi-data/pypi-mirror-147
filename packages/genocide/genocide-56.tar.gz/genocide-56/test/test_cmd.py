# This file is placed in the Public Domain.


"command"


import inspect
import unittest


from genocide.callback import Cbs
from genocide.cls import Cls
from genocide.command import Cmd
from genocide.event import Event
from genocide.function import format
from genocide.handler import Handler, dispatch
from genocide.kernel import Cfg
from genocide.object import Object, get, values
from genocide.table import Tbl
from genocide.thread import launch


events = []


param = Object()
param.add = ["test@shell", "bart", ""]
param.cfg = ["nick=gcid", "server=localhost", ""]
param.dlt = ["root@shell"]
param.dne = ["test4", ""]
param.dpl = ["reddit title,summary,link"]
param.flt = ["0", ""]
param.fnd = ["cfg", "log", "rss", "cfg server==localhost", "rss rss==reddit"]
param.log = ["test1", ""]
param.met = ["root@shell"]
param.nck = ["gcid"]
param.pwd = ["bart blabla"]
param.rem = ["reddit", ""]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["things todo"]


class CLI(Handler):

     def __init__(self):
         Handler.__init__(self)

     def raw(self, txt):
         if Cfg.verbose:
             print(txt)
        
         
c = CLI()


def consume(events):
    fixed = []
    res = []
    for e in events:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            events.remove(f)
        except ValueError:
            continue
    return res


class Test_Commands(unittest.TestCase):

    def setUp(self):
        c.start()
        
    def tearDown(self):
        c.stop()

    def test_commands(self):
        cmds = sorted(Cmd.cmd)
        for cmd in cmds:
            for ex in getattr(param, cmd, [""]):
                e = Event()
                e.txt = cmd + " " + ex
                e.orig = repr(c)
                launch(Cbs.callback(e))
                events.append(e)
        consume(events)
        self.assertTrue(not events)
