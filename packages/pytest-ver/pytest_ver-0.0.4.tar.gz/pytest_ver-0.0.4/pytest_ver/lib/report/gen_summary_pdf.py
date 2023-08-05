import os

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Table, TableStyle

from .. import services
from ..report.gen_base_pdf import GenBasePdf


# -------------------
class GenSummaryPdf(GenBasePdf):
    # -------------------
    def __init__(self, summary):
        self._summary = summary

        # TODO roll the file
        path = os.path.join(services.cfg.outdir, 'summary.pdf')

        self._doc_init(path)

    # -------------------
    def gen(self):
        self._gen_test_run_details()
        self._gen_title('Summary')

        self._gen_req_summary()

        self._gen_proto_summary()

        self._build()

    # -------------------
    def _gen_req_summary(self):
        tbl = []
        tbl.append([
            Paragraph('<b>Requirements Summary</b>', self._style_sheet['BodyText'])
        ])

        # total requirements
        tbl.append(['', 'Count', 'Percentage'])

        # total requirements
        total = len(self._summary['reqid'])
        msg = '#Requirements'
        pct = '100.0%'
        tbl.append([msg, total, pct])

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
        tbl.append([msg, num_passing, f'{pct}%'])

        # report failing
        if total == 0:
            pct = 0
        else:
            pct = round((num_failing * 100.0) / total, 1)
        msg = '#Requirements FAIL'
        tbl.append([msg, num_failing, f'{pct}%'])

        # TODO report: total #Requirements missing, % reqmts with no results

        self._gen_summary_table(tbl)

    # -------------------
    def _gen_proto_summary(self):
        tbl = []
        tbl.append([
            Paragraph('<b>Protocol Summary</b>', self._style_sheet['BodyText'])
        ])

        # total requirements
        tbl.append(['', 'Count', 'Percentage'])

        # total protocols
        total = len(self._summary['protoid'])
        msg = '#Protocols'
        pct = '100.0%'
        tbl.append([msg, total, pct])

        # count failing/passing reqmts
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
        tbl.append([msg, num_passing, f'{pct}%'])

        # report failing
        if total == 0:
            pct = 0
        else:
            pct = round((num_failing * 100.0) / total, 1)
        msg = '#Protocols FAIL'
        tbl.append([msg, num_failing, f'{pct}%'])

        # TODO ??report: total #Protocols skipped, % protos skipped

        self._gen_summary_table(tbl)

    # -------------------
    def _gen_summary_table(self, tbl):
        tbl_widths = [
            3.20 * inch,  # desc
            0.50 * inch,  # value
            0.85 * inch,  # pct
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

                # top row spans all columns
                ('BACKGROUND', (0, 0), (2, 0), colors.lightblue),
                ('SPAN', (0, 0), (2, 0)),

                # 2nd row is a title row
                ('BACKGROUND', (0, 1), (2, 1), colors.lightgrey),

                # "description" column is middle/center
                ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),

                # "value" column is middle/right
                ('VALIGN', (1, 0), (1, -1), 'MIDDLE'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),

                # "%" column is middle/right
                ('VALIGN', (2, 0), (2, -1), 'MIDDLE'),
                ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ]
        ))
        self._elements.append(t)
