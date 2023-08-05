import datetime
import os

from .. import services


# -------------------
class Logger:
    # -------------------
    def __init__(self):
        self._fp = None
        self._line_count = 0
        self._dts_count = 0
        self._dts_last = None

    # -------------------
    def init(self):
        path = os.path.join(services.cfg.outdir, 'pytest_ver.log')
        self._fp = open(path, 'w')

    # -------------------
    def start(self, msg):
        self._write_line('====', msg, so=False)

    # -------------------
    def line(self, msg):
        self._write_line(' ', msg, so=False)

    # -------------------
    def warn(self, msg):
        self._write_line('WARN', msg, so=True)

    # -------------------
    def err(self, msg):
        self._write_line('ERR', msg, so=True)

    # -------------------
    def dbg(self, msg):
        self._write_line('DBG', msg, so=False)

    # -------------------
    def _write_line(self, tag, msg, so=False):
        if self._dts_count == 0:
            # capture the current dts and save it for doing the delta per line
            self._dts_last = datetime.datetime.now(datetime.timezone.utc)
            dts = self._dts_last.astimezone().strftime(services.cfg.dts_format)

            # print dts
            line = f'{"----": <4} {dts}'
            self._fp.write(f'{line}\n')

            # print full dts every so often
            self._dts_count = 100

        line = f'{tag: <4} {msg}'

        self._dts_count -= 1

        # add time delta to log lines
        diff = datetime.datetime.now(datetime.timezone.utc) - self._dts_last
        self._fp.write(f'{diff} {line}\n')

        # ok to flush?
        self._line_count += 1
        if self._line_count > 5:
            self._fp.flush()

        # ok to write to stdout?
        if so:
            print(line)
