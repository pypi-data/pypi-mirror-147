import json
import os
import re

import jsmin

from pytest_ver.lib.report.page_info import PageInfo
from . import services


# -------------------
class Cfg:
    # -------------------
    def __init__(self):
        # --- Public - default settings
        self.outdir = 'out'
        self.storage_type = 'dev'
        # one of formal, dryrun, dev
        self.test_run_type = 'dev'
        self.test_run_id = 'dev-001'
        self.dts_format = "%Y-%m-%d %H:%M:%S %Z"
        self.page_info = PageInfo()
        self.test_name = 'unknown'
        self.reqmt_json_path = None

    # -------------------
    def init(self):
        self._read_ini()

    # -------------------
    def init2(self):
        # eg.  ver/test_sample_ver1.py
        m = re.search(r'test_(\w+)\.py::(\w+)', os.getenv('PYTEST_CURRENT_TEST'))
        if m:
            self.test_name = m.group(1)
        else:
            self.test_name = 'unknown'

    # -------------------
    def report(self):
        services.logger.start('Cfg:')
        services.logger.line(f"  {'Output Dir': <20}: {self.outdir}")
        services.logger.line(f"  {'Storage Type': <20}: {self.storage_type}")
        services.logger.line(f"  {'Test Run Id': <20}: {self.test_run_id}")
        services.logger.line(f"  {'Test Name': <20}: {self.test_name}")
        services.logger.line(f"  {'Req. json path': <20}: {self.reqmt_json_path}")

        services.logger.line('')

    # -------------------
    def _read_ini(self):
        path = 'cfg.json'
        if not os.path.isfile(path):
            # TODO convert to loggerstdout
            services.logger.warn(f'{path} not found')
            return

        # load json file
        with open(path, 'r') as fp:
            cleanj = jsmin.jsmin(fp.read())
            j = json.loads(cleanj)

        # override and/or add to available attributes
        for key, value in j.items():
            if key == 'tp_results':
                self.page_info.init_tp_result(value)
            elif key == 'trace':
                self.page_info.init_trace(value)
            elif key == 'summary':
                self.page_info.init_summary(value)
            else:
                setattr(self, key, value)
