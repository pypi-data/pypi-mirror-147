import os

from .gen_base_txt import GenBaseTxt
from .. import services


# -------------------
class GenSummaryTxt(GenBaseTxt):
    # -------------------
    def __init__(self, summary):
        super().__init__()
        self._summary = summary

        # TODO roll the file
        self._path = os.path.join(services.cfg.outdir, 'summary.txt')

    # -------------------
    def gen(self):
        services.logger.start('report: summary')

        fp = open(self._path, 'w')
        self._gen_test_run_details(fp)
        self._gen_title(fp, 'Summary')

        # TODO add detailed flag?
        self._gen_req_summary(fp)
        fp.write(f'\n')
        self._gen_proto_summary(fp)

        fp.close()

    # -------------------
    def _gen_req_summary(self, fp):
        # total requirements
        total = len(self._summary['reqid'])
        msg = '#Requirements'
        pct = 100.0
        self._write_line(fp, msg, total, pct)

        # cound failing/passing reqmts
        num_failing = 0
        num_passing = 0
        for reqids, item in self._summary['reqid'].items():
            if item['result'] == 'FAIL':
                num_failing += 1
            else:
                num_passing += 1

        # report passing
        if total == 0:
            pct = 0
        else:
            pct = round((num_passing * 100.0) / total, 1)
        msg = '#Requirements PASS'
        self._write_line(fp, msg, num_passing, pct)

        # report failing
        if total == 0:
            pct = 0
        else:
            pct = round((num_failing * 100.0) / total, 1)
        msg = '#Requirements FAIL'
        self._write_line(fp, msg, num_failing, pct)

        # TODO report: total #Requirements missing, % reqmts with no results

    # -------------------
    def _gen_proto_summary(self, fp):
        # total protocols
        total = len(self._summary['protoid'])
        msg = '#Protocols'
        pct = 100.0
        self._write_line(fp, msg, total, pct)

        # cound failing/passing reqmts
        num_failing = 0
        num_passing = 0
        for reqids, item in self._summary['protoid'].items():
            if item['result'] == 'FAIL':
                num_failing += 1
            else:
                num_passing += 1

        # report passing
        if total == 0:
            pct = 0
        else:
            pct = round((num_passing * 100.0) / total, 1)
        msg = '#Protocols PASS'
        self._write_line(fp, msg, num_passing, pct)

        # report failing
        if total == 0:
            pct = 0
        else:
            pct = round((num_failing * 100.0) / total, 1)
        msg = '#Protocols FAIL'
        self._write_line(fp, msg, num_failing, pct)

        # TODO ??report: total #Protocols skipped, % protos skipped

    # -------------------
    def _write_line(self, fp, msg, val, pct):
        fp.write(f'{msg: <20}: {val: >3}  {pct: >6}%\n')
