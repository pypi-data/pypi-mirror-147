import os

from .gen_base_txt import GenBaseTxt
from .. import services
from ..result_summary import ResultSummary


# -------------------
class GenTpTxt(GenBaseTxt):
    # -------------------
    def __init__(self, protocols):
        super().__init__()
        self._protocols = protocols

        # TODO roll the file
        self._path = os.path.join(services.cfg.outdir, 'tp_results.txt')

    # -------------------
    def gen(self):
        # TODO add detailed flag

        services.logger.start('report: TP results')
        # uncomment to debug:
        # services.logger.dbg(f'protocols: {json.dumps(self._protocols, indent=2)}')

        fp = open(self._path, 'w')
        self._gen_test_run_details(fp)
        self._gen_title(fp, 'Test Protocols with results')

        for protocol in self._protocols:
            fp.write(f'==== protocol: {protocol["desc"]}\n')
            stepno = 0
            for step in protocol['steps']:
                stepno += 1
                fp.write(f'     Step {stepno: <3}: {step["desc"]}\n')
                fp.write(f'       > dts     : {step["dts"]}\n')

                # default is a passed, and empty result
                rs = ResultSummary()
                rs.passed()
                for res in step['results']:
                    rs = ResultSummary()
                    rs.load(res)
                    if rs.result == 'FAIL':
                        break
                fp.write(f'       > result  : {rs.result}\n')
                fp.write(f'       > actual  : {rs.actual}\n')
                fp.write(f'       > expected: {rs.expected}\n')
                fp.write(f'       > reqids  : {rs.reqids}\n')
                fp.write(f'       > location: {rs.location}\n')
            fp.write(f'\n')
        fp.close()
