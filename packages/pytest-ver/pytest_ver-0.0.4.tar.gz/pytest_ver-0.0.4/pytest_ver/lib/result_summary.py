# -------------------
class ResultSummary(dict):
    # -------------------
    def __init__(self):
        super().__init__()
        self.result = 'PASS'
        self.actual = None
        self.expected = None
        self.reqids = None
        self.location = None

    # -------------------
    def load(self, j):
        self.result = j['result']
        self.actual = j['actual']
        self.expected = j['expected']
        self.reqids = j['reqids']
        self.location = j['location']

    # -------------------
    def passed(self):
        self.result = 'PASS'

    # -------------------
    def failed(self):
        self.result = 'FAIL'

    # -------------------
    def set_reqids(self, reqids):
        if reqids is None:
            self.reqids = None
        elif isinstance(reqids, str):
            self.reqids = [reqids]
        elif isinstance(reqids, list):
            self.reqids = reqids

    # -------------------
    ## required for JSON to handle this class as a dictionary
    def __setattr__(self, key, value):
        self[key] = value

    # -------------------
    ## required for JSON to handle this class as a dictionary
    def __getattr__(self, key):
        return self[key]
