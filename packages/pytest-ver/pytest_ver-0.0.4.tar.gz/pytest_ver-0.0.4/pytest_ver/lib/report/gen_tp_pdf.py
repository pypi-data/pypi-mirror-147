import json
import os

import jsmin
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, ListItem, Paragraph, Table, TableStyle

from .gen_base_pdf import GenBasePdf
from .. import services
from ..result_summary import ResultSummary


# -------------------
class GenTpPdf(GenBasePdf):
    # -------------------
    def __init__(self, protocols):
        self._requirements = []

        self._protocols = protocols
        path = os.path.join(services.cfg.outdir, 'tp_results.pdf')
        self._doc_init(path)

    # -------------------
    def gen(self):
        # TODO move into it's own class
        if services.cfg.reqmt_json_path is not None:
            with open(services.cfg.reqmt_json_path, 'r', encoding='utf-8') as fp:
                cleanj = jsmin.jsmin(fp.read())
                self._requirements = json.loads(cleanj)

        self._gen_test_run_details()
        self._gen_title('Test Protocols with results')

        for protocol in self._protocols:
            self._gen_protocol(protocol)

        self._build()

    # -------------------
    def _gen_protocol(self, protocol):
        tbl = []

        # row 0
        tbl.append([
            Paragraph(f"<b>{protocol['proto_id']}</b>: {protocol['desc']}", self._style_sheet['BodyText']),
            '', '', '',
            Paragraph(f"<b>Start date:</b>: {protocol['start_date']}", self._style_sheet['BodyText']),
            '', '',
        ])

        # row 1
        tbl.append([
            Paragraph(f"<b>Executed by</b>: {protocol['executed_by']}", self._style_sheet['BodyText']),
            '', '', '',
            Paragraph(f"<b>Requirements:</b>: see below", self._style_sheet['BodyText']),
            '', '',
        ])

        # row 2
        tbl.append([
            Paragraph(f"<b>Software Version</b>: {protocol['dut_version']}", self._style_sheet['BodyText']),
            '', '', '',
            Paragraph(f"<b>Serial number:</b> {protocol['dut_serialno']}",
                      self._style_sheet['BodyText']),
            '', '',
        ])

        # row 3
        tbl.append([
            self._gen_list('Objectives', protocol['objectives']),
            '', '', '', '', '',
        ])

        # row 4
        tbl.append([
            self._gen_list('Preconditions', protocol['preconditions']),
            '', '', '',
            self._gen_list('Deviations', protocol['deviations']),
            '', '',
        ])

        # row 5: title row
        tbl.append(
            [
                Paragraph('<b>Step</b>'),
                Paragraph('<b>Req.</b>'),
                Paragraph('<b>Execution Instructions</b>'),
                Paragraph('<b>Expected</b>'),
                Paragraph('<b>Actual</b>'),
                Paragraph('<b>Pass /\nFail</b>'),
                Paragraph('<b>Date</b>')
            ]
        )

        requirements = []
        stepno = 0
        for step in protocol['steps']:
            stepno += 1
            self._gen_step(tbl, stepno, step, requirements)

        self._gen_protocol_table(tbl)
        self._gen_reqmt_table(requirements)

    # -------------------
    def _gen_list(self, tag, items):
        paragraph_text = f'<b>{tag}</b>'
        paragraph_style = self._style_sheet['BodyText']
        if len(items) == 0:
            list_items = 'N/A'
            paragraph = Paragraph(f"{paragraph_text}: {list_items}", paragraph_style)
        elif len(items) == 1:
            list_items = items[0]
            paragraph = Paragraph(f"{paragraph_text}: {list_items}", paragraph_style)
        else:
            # more than 1 item in the list
            paragraph = [
                Paragraph(f"{paragraph_text}:", paragraph_style),
            ]
            list_items = []
            for item in items:
                list_items.append(ListItem(Paragraph(item)))
            paragraph.append(ListFlowable(list_items, bulletType='bullet'))

        return paragraph

    # -------------------
    def _gen_step(self, tbl, stepno, step, requirements):
        # default is a passed, and empty result
        rs = ResultSummary()
        rs.passed()
        for res in step['results']:
            rs = ResultSummary()
            rs.load(res)
            if rs.result == 'FAIL':
                break

        desc = Paragraph(step['desc'], self._style_sheet['BodyText'])
        result = rs.result
        actual = rs.actual
        expected = rs.expected
        details = str(step['dts']) + '\n'
        details += str(rs.location)
        if rs.reqids is None:
            reqids_str = 'N/A'
        else:
            for reqid in rs.reqids:
                if reqid not in requirements:
                    requirements.append(reqid)
            if len(rs.reqids) == 1:
                reqids_str = Paragraph(rs.reqids[0], self._style_sheet['BodyText'])
            else:
                reqids_str = Paragraph('<br/>'.join(rs.reqids), self._style_sheet['BodyText'])

        tbl.append([stepno, reqids_str, desc, expected, actual, result, details])

    # -------------------
    def _gen_protocol_table(self, tbl):
        if services.cfg.page_info.orientation == 'portrait':
            # portrait: should be 7.5"
            tbl_widths = [
                0.50 * inch,  # stepno
                0.85 * inch,  # reqmt.
                1.65 * inch,  # desc
                1.15 * inch,  # expected
                1.15 * inch,  # actual
                0.50 * inch,  # result
                1.70 * inch,  # details
            ]
        else:
            # landscape (10" width)
            tbl_widths = [
                0.50 * inch,  # stepno
                0.85 * inch,  # reqmt.
                4.15 * inch,  # desc
                1.15 * inch,  # expected
                1.15 * inch,  # actual
                0.50 * inch,  # result
                1.70 * inch,  # details
            ]

        # uncomment to debug
        # total = 0.0
        # for val in tbl_widths:
        #     total += val
        # there are 72 per inch
        # print(f"JAX: {total / 72}")

        t = Table(tbl,
                  colWidths=tbl_widths,
                  spaceBefore=0.25 * inch,
                  spaceAfter=0.0 * inch,
                  )

        t.setStyle(TableStyle(
            [
                # borders
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black),

                # row 0: spans 2 cols, tp info and desc
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('SPAN', (0, 0), (4, 0)),
                ('SPAN', (4, 0), (-1, 0)),
                ('INNERGRID', (0, 0), (3, 0), 0.25, colors.black),

                # row 1: spans 2 cols, executed_by and requirements
                ('BACKGROUND', (0, 1), (-1, 1), colors.lightblue),
                ('SPAN', (0, 1), (4, 1)),
                ('SPAN', (4, 1), (-1, 1)),

                # row 2: spans 2 cols, version and serialno
                ('BACKGROUND', (0, 2), (-1, 2), colors.lightblue),
                ('SPAN', (0, 2), (4, 2)),
                ('SPAN', (4, 2), (-1, 2)),

                # row 3: spans all cols, objectives
                ('BACKGROUND', (0, 3), (-1, 3), colors.lightblue),
                ('SPAN', (0, 3), (-1, 3)),

                # row 4: spans 2 cols, preconditions and deviations
                ('BACKGROUND', (0, 4), (-1, 4), colors.lightblue),
                ('SPAN', (0, 4), (4, 4)),
                ('SPAN', (4, 4), (-1, 4)),

                # use borders from now on
                # row 5: title row with all columns
                ('BACKGROUND', (0, 5), (-1, 5), colors.lightgrey),

                # row 6 and on
                ('VALIGN', (0, 6), (0, -1), 'MIDDLE'),  # 0: stepno ; middle/center
                ('ALIGN', (0, 6), (0, -1), 'CENTER'),
                ('VALIGN', (1, 6), (1, -1), 'MIDDLE'),  # 1: reqmt
                ('VALIGN', (2, 6), (2, -1), 'MIDDLE'),  # 2: desc
                ('VALIGN', (3, 6), (3, -1), 'MIDDLE'),  # 3: expected
                ('VALIGN', (4, 6), (4, -1), 'MIDDLE'),  # 4: actual
                ('VALIGN', (5, 6), (5, -1), 'MIDDLE'),  # 5: result ; middle/center
                ('ALIGN', (5, 6), (5, -1), 'CENTER'),
                ('VALIGN', (6, 6), (6, -1), 'MIDDLE'),  # details
            ]
        ))
        self._elements.append(t)

    # -------------------
    def _gen_reqmt_table(self, requirements):
        if services.cfg.page_info.orientation == 'portrait':
            # portrait: 7.5"
            tbl_widths = [
                0.85 * inch,  # reqmt.
                6.65 * inch,  # desc
            ]
        else:
            # landscape: 10"
            tbl_widths = [
                0.85 * inch,  # reqmt.
                9.15 * inch,  # desc
            ]

        tbl = []

        # row 0: title row
        tbl.append(
            [
                Paragraph('<b>Req.</b>'),
                Paragraph('<b>Desc.</b>'),
            ]
        )

        for reqmt in sorted(requirements):
            if reqmt in self._requirements:
                tbl.append([reqmt, Paragraph(self._requirements[reqmt]['desc'])])
            else:
                tbl.append([reqmt, Paragraph(f'Could not find {reqmt} in file: {services.cfg.reqmt_json_path}')])

        t = Table(tbl,
                  colWidths=tbl_widths,
                  spaceBefore=0.1 * inch,
                  spaceAfter=0.50 * inch,
                  )

        t.setStyle(TableStyle(
            [
                # borders
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black),

                # use borders from now on
                # row 0: title row with all columns
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),

                # row 1 and on
                ('VALIGN', (0, 1), (0, -1), 'MIDDLE'),  # col 0: reqmt
                ('VALIGN', (1, 1), (1, -1), 'MIDDLE'),  # col 1: desc
            ]
        ))

        self._elements.append(t)
