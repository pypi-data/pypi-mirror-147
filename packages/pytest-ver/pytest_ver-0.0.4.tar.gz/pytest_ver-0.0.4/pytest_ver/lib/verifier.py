import os
import sys
import types

from . import services
from .result_summary import ResultSummary


# -------------------
class Verifier:
    # -------------------
    def verify(self, actual, reqids=None):
        rs, tb = self._create_result_summary(reqids)

        rs.actual = actual
        rs.expected = True

        if actual:
            self._handle_pass(rs)
        else:
            self._handle_fail(rs, tb)

    # -------------------
    def verify_equal(self, expected, actual, reqids=None):
        rs, tb = self._create_result_summary(reqids)

        rs.actual = actual
        rs.expected = expected

        if actual == expected:
            self._handle_pass(rs)
        else:
            self._handle_fail(rs, tb)

    # -------------------
    def _handle_pass(self, rs):
        self._save_result_pass(rs)

    # -------------------
    def _handle_fail(self, rs, tb):
        self._save_result_fail(rs)

        # Throw an assertion so the pyunit stops and shows a stack trace
        # starting from the verify_x() command in the caller
        raise AssertionError().with_traceback(tb)

    # -------------------
    def _save_result_pass(self, rs):
        rs.passed()
        services.proto.add_result(rs)

    # -------------------
    def _save_result_fail(self, rs):
        rs.failed()
        services.proto.add_result(rs)

    # -------------------
    def _create_result_summary(self, reqids):
        # get a full stackframe
        try:
            raise AssertionError
        except AssertionError:
            tb = sys.exc_info()[2]

        # go two callers back
        frame = tb.tb_frame
        frame = frame.f_back
        frame = frame.f_back

        tb = types.TracebackType(tb_next=None,
                                 tb_frame=frame,
                                 tb_lasti=frame.f_lasti,
                                 tb_lineno=frame.f_lineno)

        # uncomment to debug
        # print(f"\nDBG: {frame.f_code.co_name}")
        # print(f"DBG: {frame.f_code.co_filename}")
        # print(f"DBG: {frame.f_lineno}")

        fname = os.path.basename(frame.f_code.co_filename)
        location = f'{fname}({frame.f_lineno})'

        # create a results summary and pre-populate it
        rs = ResultSummary()
        rs.location = location
        rs.set_reqids(reqids)

        return rs, tb
