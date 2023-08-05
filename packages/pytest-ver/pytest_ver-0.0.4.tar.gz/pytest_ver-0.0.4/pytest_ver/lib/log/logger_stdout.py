# -------------------
class LoggerStdout:
    # -------------------
    def init(self):
        pass

    # -------------------
    def start(self, msg):
        self._write_line('====', msg)

    # -------------------
    def line(self, msg):
        self._write_line(' ', msg)

    # -------------------
    def warn(self, msg):
        self._write_line('WARN', msg)

    # -------------------
    def err(self, msg):
        self._write_line('ERR', msg)

    # -------------------
    def dbg(self, msg):
        self._write_line('DBG', msg)

    # -------------------
    def _write_line(self, tag, msg):
        print(f'{tag: <4} {msg}')
