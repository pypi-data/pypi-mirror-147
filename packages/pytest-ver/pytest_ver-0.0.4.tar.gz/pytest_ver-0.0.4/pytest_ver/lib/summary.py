from . import services


# -------------------
class Summary:
    # -------------------
    def __init__(self):
        self._summary = {
            'reqid': {},
            'protoid': {},
        }

    # -------------------
    def term(self):
        self.save()

    # -------------------
    def add_result(self, reqids, protoid, result):
        if reqids is not None:
            for reqid in reqids:
                if reqid in self._summary['reqid']:
                    self._reqid_add_to(reqid, result)
                else:
                    self._reqid_add(reqid, result)

        if protoid in self._summary['protoid']:
            self._protoid_add_to(protoid, result)
        else:
            self._protoid_add(protoid, result)

        self.save()

    # -------------------
    def _reqid_add(self, reqid, result):
        self._summary['reqid'][reqid] = {
            'count': 1,
            'result': result
        }

    # -------------------
    def _reqid_add_to(self, reqid, result):
        self._summary['reqid'][reqid]['count'] += 1
        if self._summary['reqid'][reqid]['result'] == 'PASS':
            self._summary['reqid'][reqid]['result'] = result
        # if FAIL, stays FAIL

    # -------------------
    def _protoid_add(self, protoid, result):
        self._summary['protoid'][protoid] = {
            'count': 1,
            'result': result
        }

    # -------------------
    def _protoid_add_to(self, protoid, result):
        self._summary['protoid'][protoid]['count'] += 1
        if self._summary['protoid'][protoid]['result'] == 'PASS':
            self._summary['protoid'][protoid]['result'] = result
        # if FAIL, stays FAIL

    # -------------------
    def save(self):
        services.storage.save_summary(self._summary)
