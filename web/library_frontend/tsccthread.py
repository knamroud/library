from threading import Thread, Event
from subprocess import run
from os import remove, listdir
from os.path import exists, join, getmtime


class TSCCThread(Thread):
    def __init__(self, tspath: str, jspath: str, flags: str = " ", debug: bool = False):
        Thread.__init__(self)
        self.tsp = tspath
        self.jsp = jspath
        self.flags = flags.split(" ")
        self.debug = debug
        self._stop_event = Event()

    def run(self):
        while not self._stop_event.is_set():
            for file in listdir(self.tsp):
                if file.find(".") == 0:
                    continue
                elif file.split(".")[-1] != "ts":
                    remove(join(self.tsp, file))
                    continue
                js = join(self.jsp, file.replace("ts", "js"))
                ts = join(self.tsp, file)
                if not exists(js) or getmtime(js) < getmtime(ts):
                    print(f" * Detected change in '{ts}', recompiling.")
                    run(["tsc", ts, "--outFile", js]+self.flags)
            for file in listdir(self.jsp):
                if not exists(join(self.tsp, file.replace("js", "ts"))):
                    remove(join(self.jsp, file))
            if not self.debug:
                break

    def stop(self):
        self._stop_event.set()
