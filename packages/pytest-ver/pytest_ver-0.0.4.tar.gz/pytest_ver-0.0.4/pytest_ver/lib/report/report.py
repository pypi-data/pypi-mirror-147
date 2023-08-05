from .. import services
from ..report.gen_summary_pdf import GenSummaryPdf
from ..report.gen_summary_txt import GenSummaryTxt
from ..report.gen_tp_pdf import GenTpPdf
from ..report.gen_tp_txt import GenTpTxt
from ..report.gen_trace_matrix_pdf import GenTraceMatrixPdf
from ..report.gen_trace_matrix_txt import GenTraceMatrixTxt


# -------------------
class Report:
    def __init__(self):
        pass

    # -------------------
    def report(self):
        self._report_protocols()
        self._report_trace_matrix()
        self._report_summary()

    # -------------------
    # gen protocols with results
    def _report_protocols(self):
        services.cfg.page_info.set_tp_cfg()
        protocols = services.storage.get_protocols()

        gtt = GenTpTxt(protocols)
        gtt.gen()

        gtp = GenTpPdf(protocols)
        gtp.gen()

    # -------------------
    # trace matrix
    def _report_trace_matrix(self):
        services.cfg.page_info.set_trace_cfg()
        matrix = services.storage.get_trace()

        gtt = GenTraceMatrixTxt(matrix)
        gtt.gen()

        gtm = GenTraceMatrixPdf(matrix)
        gtm.gen()

    # -------------------
    # summary
    def _report_summary(self):
        services.cfg.page_info.set_summary_cfg()
        summary = services.storage.get_summary()

        gst = GenSummaryTxt(summary)
        gst.gen()

        gsp = GenSummaryPdf(summary)
        gsp.gen()
