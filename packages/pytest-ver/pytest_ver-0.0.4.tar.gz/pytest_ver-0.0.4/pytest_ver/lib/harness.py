import pytest

from . import services
from .cfg import Cfg
from .log.logger import Logger
from .log.logger_stdout import LoggerStdout
from .protocol import Protocol
from .report.report import Report
from .storage.storage import Storage
from .summary import Summary
from .trace_matrix import TraceMatrix
from .verifier import Verifier


# -------------------
class PytestHarness:
    # -------------------
    def __init__(self):
        services.harness = self

        services.logger = LoggerStdout()
        services.logger.init()

        services.cfg = Cfg()
        services.cfg.init()

        # after cfg indicates where log files are stored
        # can use normal logger
        services.logger = Logger()
        services.logger.init()

        services.storage = Storage.factory()
        services.summary = Summary()
        services.trace = TraceMatrix()
        services.proto = Protocol()
        self.proto = services.proto
        self.ver = Verifier()

    # -------------------
    def init(self):
        services.cfg.init2()
        services.cfg.report()

        services.storage.init()

    # -------------------
    def term(self):
        services.proto.term()
        services.trace.term()
        services.summary.term()
        services.storage.term()

    # -------------------
    def report(self):
        rep = Report()
        rep.report()

    # -------------------
    def abort(self):
        services.logger.err('abort called')
        pytest.exit('abort called')
