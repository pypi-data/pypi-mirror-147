import datetime

from . import services


# -------------------
class Protocol:
    # -------------------
    def __init__(self):
        self._protocols = []
        self._protocol = None
        self._step = None

    # -------------------
    def term(self):
        self.save()

    # -------------------
    def protocol(self, proto_id: str, desc):
        now = datetime.datetime.now(datetime.timezone.utc)
        dts = now.strftime('%Y-%m-%d %H:%M:%S')
        self._protocol = {
            'proto_id': proto_id.upper(),
            'desc': desc,
            'executed_by': 'automated',
            'start_date': dts,
            'dut_version': 'N/A',
            'dut_serialno': 'N/A',
            'objectives': [],
            'preconditions': [],
            'deviations': [],
            'steps': [],
        }
        self._protocols.append(self._protocol)
        self._step = None
        self.save()

    # -------------------
    def set_version(self, version):
        self._protocol['dut_version'] = version

    # -------------------
    def set_serialno(self, serialno):
        self._protocol['dut_serialno'] = serialno

    # -------------------
    def add_objective(self, objective):
        self._protocol['objectives'].append(objective)

    # -------------------
    def add_precondition(self, precondition):
        self._protocol['preconditions'].append(precondition)

    # -------------------
    def add_deviation(self, deviation):
        self._protocol['deviations'].append(deviation)

    # -------------------
    def step(self, desc):
        now = datetime.datetime.now(datetime.timezone.utc)
        dts = now.strftime('%Y-%m-%d %H:%M:%S')
        self._step = {
            'desc': desc,
            'dts': dts,
            'results': [],
        }
        self._protocol['steps'].append(self._step)
        self.save()

    # -------------------
    def add_result(self, rs):
        services.logger.dbg(f'{rs.result}: reqids:{rs.reqids} actual:{rs.actual} expected:{rs.expected}')
        self._step['results'].append(rs)
        if rs.reqids is not None:
            services.trace.add_proto(rs.reqids, self._protocol['proto_id'], rs.location)
        services.summary.add_result(rs.reqids, self._protocol['proto_id'], rs.result)
        self.save()

    # -------------------
    def save(self):
        services.storage.save_protocol(self._protocols)
