import os

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Table, TableStyle

from .gen_base_pdf import GenBasePdf
from .. import services


# -------------------
class GenTraceMatrixPdf(GenBasePdf):
    # -------------------
    def __init__(self, matrix):
        self._matrix = matrix
        path = os.path.join(services.cfg.outdir, 'trace.pdf')

        self._doc_init(path)

    # -------------------
    def gen(self):
        self._gen_test_run_details()
        self._gen_title('Trace Matrix')

        self._gen_trace_table()

        # TODO delete
        # p = Paragraph('TODO paragraph after the table?', self._style_sheet['BodyText'])
        # self._elements.append(p)

        self._build()

    # -------------------
    def _gen_trace_table(self):
        tbl = []
        tbl.append(
            [
                Paragraph('<b>Req. Id</b>'),
                Paragraph('<b>Protocol</b>'),
            ]
        )

        for req_id in sorted(self._matrix.keys()):
            self._gen_row(tbl, req_id, self._matrix[req_id])

        self._gen_table(tbl)

    # -------------------
    def _gen_row(self, tbl, req_id, proto):
        newline = False
        proto_info = ''
        for proto in sorted(self._matrix[req_id], key=lambda item: item['proto_id']):
            if newline:
                proto_info += '\n'
            proto_info += f"{proto['proto_id']} {proto['proto_info']}"
            newline = True

        tbl.append([req_id, proto_info])

    # -------------------
    def _gen_table(self, tbl):
        tbl_widths = [
            0.75 * inch,  # reqid
            6.25 * inch,  # proto_info
        ]

        t = Table(tbl,
                  colWidths=tbl_widths,
                  spaceBefore=0.25 * inch,
                  spaceAfter=0.25 * inch,
                  )

        t.setStyle(TableStyle(
            [
                # borders
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),

                # 1st row is a title row
                ('BACKGROUND', (0, 1), (5, 1), colors.lightgrey),

                # "reqid" column
                ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),

                # "protocol" column
                ('VALIGN', (1, 0), (1, -1), 'MIDDLE'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ]
        ))
        self._elements.append(t)
