# This file is placed in the Public Domain.


"command tests"


import inspect
import random
import unittest


from ocb import Callback
from ocl import Class
from odb import Config
from oev import Event
from ofn import format
from ohd import Handler
from obj import Object, get, keys, values
from otb import Table
from oth import launch


events = []
cmds = "commands,delete,display,fetch,find,fleet,log,meet,more,remove,rss,threads,todo"


param = Object()
param.commands = [""]
param.config = ["nick=opbot", "server=localhost", "port=6699"]
param.display = ["reddit title,summary,link", ""]
param.fetch = [""]
param.find = ["log", "log txt==test", "rss", "rss rss==reddit", "config server==localhost"]
param.fleet = ["0", ""]
param.log = ["test1", "test2"]
param.meet = ["root@shell", "test@user"]
param.more = [""]
param.nick = ["dfly", "dflybot", "dfly_"]
param.password = ["bart blabla"]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.todo = ["things todo"]


def getmain(name):
    main =  __import__("__main__")
    return getattr(main, name, None)

         
c = getmain("c")
c.threaded = True
c.start()


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


    def test_commands(self):
        cmds = sorted(Command.cmd)
        random.shuffle(cmds)
        for cmd in cmds:
            for ex in get(param, cmd, [""]):
                e = Event()
                e.txt = cmd + " " + ex
                e.orig = repr(c)
                try:
                    Callback.callback(e)
                except Raise:
                    pass
                events.append(e)
        #consume(events)
        #self.assertTrue(not events)

# This file is placed in the Public Domain.


"object runtime"


import inspect
import os
import sys
import termios
import time
import threading
import traceback


from obj import Object, get, keys
from obs import Bus
from ocb import Callback
from ocl import Class
from oev import Event
from ofn import register
from ohd import Handler


class Command(Object):

    cmd = Object()

    @staticmethod
    def add(command):
        register(Command.cmd, command.__name__, command)

    @staticmethod
    def get(command):
        f =  get(Command.cmd, command)
        return f

        
class CLI(Handler):

    def cmd(self, txt):
        e = Event()
        e.orig = repr(self)
        e.txt = txt
        self.handle(e)
                
    def raw(self, txt):
        print(txt)


class Console(Handler):


    def announce(self, txt):
        pass

    def handle(self, e):
        Handler.handle(self, e)
        e.wait()

    def poll(self):
        e = Event()
        e.txt = input("> ")
        e.orig = repr(self)
        return e

    def raw(self, txt):
        print(txt)

    def start(self):
        Callback.add("event", dispatch)
        Handler.start(self)


def dispatch(e):
    parse(e, e.txt)
    f = Command.get(e.cmd)
    if f:
        f(e)
        e.show()
    e.ready()


def kcmd(clt, txt):
    if not txt:
        return False
    Callback.add("event", dispatch)
    Bus.add(clt)
    e = Event()
    e.channel = ""
    e.orig = repr(clt)
    e.txt = txt
    clt.handle(e)
    e.wait()
    return e.result


def print_exc(exc):
    traceback.print_exception(type(exc), exc, exc.__traceback__)


def scan(dn):
    nm = dn.split(os.sep)[-1]
    sys.path.insert(0, nm)
    for mn in os.listdir(dn):
        if mn.endswith("~"):
            continue
        if mn.endswith("__"):
            continue
        if mn.endswith(".py"):
            mn = mn[:-3]
        mod = __import__(mn, nm)
        for k, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                Command.cmd[k] = o
        for k, clz in inspect.getmembers(mod, inspect.isclass):
            Class.add(clz)


def wait():
    while 1:
        time.sleep(1.0)
