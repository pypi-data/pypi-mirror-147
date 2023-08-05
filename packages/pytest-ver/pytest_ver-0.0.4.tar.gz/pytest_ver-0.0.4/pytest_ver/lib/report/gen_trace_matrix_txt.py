import os

from .gen_base_txt import GenBaseTxt
from .. import services


# -------------------
class GenTraceMatrixTxt(GenBaseTxt):
    # -------------------
    def __init__(self, matrix):
        super().__init__()
        self._matrix = matrix

        # TODO roll the file
        self._path = os.path.join(services.cfg.outdir, 'trace.txt')

    # -------------------
    def gen(self):
        # TODO add detailed flag?

        services.logger.start('report: trace matrix')

        fp = open(self._path, 'w')
        self._gen_test_run_details(fp)
        self._gen_title(fp, 'Trace Matrix')

        for req_id in sorted(self._matrix.keys()):
            fp.write(f'req id: {req_id}\n')
            for proto in sorted(self._matrix[req_id], key=lambda item: item['proto_id']):
                fp.write(f"   proto: {proto['proto_id']} {proto['proto_info']}\n")
            fp.write(f'\n')
        fp.close()
