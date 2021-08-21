import ctypes
import threading
import time

import pyswip
from pyswip import registerForeign


class PrologMT(pyswip.Prolog):
    """Multi-threaded (one-to-one) pyswip.Prolog ad-hoc reimpl"""
    _swipl = pyswip.core._lib

    PL_thread_self = _swipl.PL_thread_self
    PL_thread_self.restype = ctypes.c_int

    PL_thread_attach_engine = _swipl.PL_thread_attach_engine
    PL_thread_attach_engine.argtypes = [ctypes.c_void_p]
    PL_thread_attach_engine.restype = ctypes.c_int

    @classmethod
    def _init_prolog_thread(cls):
        pengine_id = cls.PL_thread_self()
        if pengine_id == -1:
            pengine_id = cls.PL_thread_attach_engine(None)
            # print("{INFO} attach pengine to thread: %d" % pengine_id)
        if pengine_id == -1:
            raise pyswip.prolog.PrologError("Unable to attach new Prolog engine to the thread")
        elif pengine_id == -2:
            print("{WARN} Single-threaded swipl build, beware!")

    class _QueryWrapper(pyswip.Prolog._QueryWrapper):
        def __call__(self, *args, **kwargs):
            PrologMT._init_prolog_thread()
            return super().__call__(*args, **kwargs)


class Tournament(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.a = ""
        self.wait = True

    def process_event(self, e, t):
        while self.wait:
            pass
        self.a = t
        print(e)
    process_event.arity = 2

    def run(self) -> None:
        prolog = PrologMT()
        prolog.consult("C:/Users/Deniz Gorur/PycharmProjects/SummerProject/simulator.pl")

        registerForeign(t.process_event)

        arr = "[set(cooperationcost(1)), set(cooperationbenefit(10)), set(starttime(0)), set(rounds(1, 2)), set(generationinfo(1, 10)), output(resultsin('resultsexp1.pl')), output(eventsin('historyexp1.pl'))]"
        list(prolog.query("run(" + arr + ")"))


t = Tournament()
t.start()


def start(to):
    while True:
        to.wait = True
        yield to.a
        to.wait = False
        print()


s = start(t)
while True:
    # print("abc", next(s))
    if next(s):
        print("abc", t.a)
    time.sleep(0.5)
