import glob
import json
import os

from .storage import Storage
from .. import services


# -------------------
class StorageDev(Storage):
    # -------------------
    def __init__(self):
        self._protocol_path = None
        self._trace_path = None
        self._summary_path = None

    # -------------------
    def init(self):
        self._protocol_path = os.path.join(services.cfg.outdir, f'{services.cfg.test_name}_protocol.json')
        self._trace_path = os.path.join(services.cfg.outdir, f'{services.cfg.test_name}_trace.json')
        self._summary_path = os.path.join(services.cfg.outdir, f'{services.cfg.test_name}_summary.json')

    # -------------------
    def term(self):
        pass

    # -------------------
    def save_protocol(self, protocols):
        with open(self._protocol_path, 'w', encoding='utf=8') as fp:
            json.dump(protocols, fp, ensure_ascii=True, indent=2)

    # -------------------
    def get_protocols(self):
        jlist = []
        for f in glob.glob(os.path.join(services.cfg.outdir, '*_protocol.json')):
            with open(f, 'r', encoding='utf=8') as fp:
                items = json.load(fp)
                # TODO callback into protocol object
                for item in items:
                    jlist.append(item)
        return jlist

    # -------------------
    def save_trace(self, trace):
        with open(self._trace_path, 'w', encoding='utf=8') as fp:
            json.dump(trace, fp, ensure_ascii=True, indent=2)

    # -------------------
    def get_trace(self):
        jlist = {}
        for f in glob.glob(os.path.join(services.cfg.outdir, '*_trace.json')):
            with open(f, 'r', encoding='utf=8') as fp:
                items = json.load(fp)

                # TODO callback into trace object
                for key in items.keys():
                    if key in jlist:
                        for item in items[key]:
                            jlist[key].append(item)
                    else:
                        jlist[key] = items[key]
        return jlist

    # -------------------
    def save_summary(self, summary):
        with open(self._summary_path, 'w', encoding='utf=8') as fp:
            json.dump(summary, fp, ensure_ascii=True, indent=2)
        pass

    # -------------------
    def get_summary(self):
        jlist = {
            'reqid': {},
            'protoid': {},
        }
        for f in glob.glob(os.path.join(services.cfg.outdir, '*_summary.json')):
            with open(f, 'r', encoding='utf=8') as fp:
                items = json.load(fp)

                # TODO callback into summary object
                reqids = items['reqid']
                for key in reqids.keys():
                    if key in jlist['reqid']:
                        jlist['reqid'][key]['count'] += 1
                        if reqids[key]['result'] == 'FAIL':
                            jlist['reqid'][key]['result'] = 'FAIL'
                    else:
                        jlist['reqid'][key] = reqids[key]

                protoids = items['protoid']
                for key in protoids.keys():
                    if key in jlist['protoid']:
                        for item in protoids[key]:
                            jlist['protoid'][key].append(item)
                    else:
                        jlist['protoid'][key] = protoids[key]

        return jlist
