import datetime

import reportlab.lib.pagesizes
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.platypus import Frame, PageTemplate, Paragraph, SimpleDocTemplate, Table, TableStyle

from .. import services


# -------------------
class GenBasePdf:

    # -------------------
    def __init__(self):
        self._doc = None
        self._style_sheet = None
        self._elements = []

        # uncomment to debug
        # services.logger.dbg(f"page_info: {services.cfg.page_info}")

    # -------------------
    def _doc_init(self, path):
        if services.cfg.page_info.page_size == 'letter':
            psize = reportlab.lib.pagesizes.LETTER
        elif services.cfg.page_info.page_size == 'a4':
            psize = reportlab.lib.pagesizes.A4
        else:
            services.logger.err(f'unknown page_size: {services.cfg.page_info.page_size}')
            services.harness.abort()

        if services.cfg.page_info.orientation == 'portrait':
            self._doc = SimpleDocTemplate(path,
                                          pagesize=psize,
                                          leftMargin=0.5 * inch,
                                          rightMargin=0.5 * inch,
                                          topMargin=0.75 * inch,
                                          bottomMargin=1.0 * inch,
                                          )
        else:
            # landscape
            self._doc = SimpleDocTemplate(path,
                                          pagesize=landscape(psize),
                                          leftMargin=0.5 * inch,
                                          rightMargin=0.5 * inch,
                                          topMargin=0.75 * inch,
                                          bottomMargin=1.0 * inch,
                                          )

        self._style_sheet = getSampleStyleSheet()
        self._style_sheet.add(ParagraphStyle(name='LeftPara',
                                             parent=self._style_sheet['Normal'],
                                             alignment=TA_LEFT))
        self._style_sheet.add(ParagraphStyle(name='CenterPara',
                                             parent=self._style_sheet['Normal'],
                                             alignment=TA_CENTER))
        self._style_sheet.add(ParagraphStyle(name='RightPara',
                                             parent=self._style_sheet['Normal'],
                                             alignment=TA_RIGHT))

        self._elements = []
        frameh = Frame(self._doc.leftMargin,
                       self._doc.bottomMargin,
                       self._doc.width,
                       self._doc.height - 2 * cm,
                       id='normal')
        pt = PageTemplate(id='test', frames=[frameh], onPage=self._header_and_footer)
        self._doc.addPageTemplates([pt])

    # -------------------
    def _header_and_footer(self, canvas, doc):
        self._header(canvas, doc)
        self._footer(canvas, doc)

    # -------------------
    def _header(self, canvas, doc):
        canvas.saveState()
        t = Table([self._get_data('header', canvas)],
                  colWidths=[
                      1.75 * inch,  # left
                      4.25 * inch,  # middle
                      1.75 * inch,  # right
                  ],
                  spaceBefore=0.1,
                  spaceAfter=0.1,
                  rowHeights=0.5 * inch,
                  )

        t.setStyle(TableStyle(
            [
                # border below only
                ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black),
                # uncomment to get field delimiters in headers/footers
                # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),

                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]
        ))

        w, h = t.wrap(doc.width, doc.topMargin)
        t.drawOn(canvas, doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - h)
        canvas.restoreState()

    # -------------------
    def _footer(self, canvas, doc):
        canvas.saveState()

        t = Table([self._get_data('footer', canvas)],
                  colWidths=[
                      1.75 * inch,  # left
                      4.25 * inch,  # middle
                      1.75 * inch,  # right
                  ],
                  spaceBefore=0.0,
                  spaceAfter=0.0,
                  )

        t.setStyle(TableStyle(
            [
                # border below only
                ('LINEABOVE', (0, 0), (-1, -1), 0.25, colors.black),
                # uncomment to get field delimiters in headers/footers
                # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),

                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]
        ))

        w, h = t.wrap(doc.width, doc.bottomMargin)
        t.drawOn(canvas, doc.leftMargin, h)

        canvas.restoreState()

    # -------------------
    def _get_data(self, tag, canvas):
        row = []
        if services.cfg.page_info[tag].left == '<pageno>':
            row.append(Paragraph(f'Page {canvas.getPageNumber()}', self._style_sheet['LeftPara']))
        else:
            row.append(Paragraph(services.cfg.page_info[tag].left, self._style_sheet['LeftPara']))

        if services.cfg.page_info[tag].middle == '<pageno>':
            row.append(Paragraph(f'Page {canvas.getPageNumber()}', self._style_sheet['CenterPara']))
        else:
            row.append(Paragraph(services.cfg.page_info[tag].middle, self._style_sheet['CenterPara']))

        if services.cfg.page_info[tag].right == '<pageno>':
            row.append(Paragraph(f'Page {canvas.getPageNumber()}', self._style_sheet['LeftPara']))
        else:
            row.append(Paragraph(services.cfg.page_info[tag].right, self._style_sheet['LeftPara']))

        return row

    # -------------------
    def _build(self):
        self._doc.build(self._elements)

    # -------------------
    def _gen_test_run_details(self):
        p = Paragraph('<b>Test Run Details</b>', self._style_sheet['BodyText'])
        self._elements.append(p)

        line = f"{'Test Run Type': <20}: {services.cfg.test_run_type}"
        p = Paragraph(line, bulletText=u'\u2022')
        self._elements.append(p)

        line = f"{'Test Run Id': <20}: {services.cfg.test_run_id}"
        p = Paragraph(line, bulletText=u'\u2022')
        self._elements.append(p)

        dts = datetime.datetime.now(datetime.timezone.utc).astimezone().strftime(services.cfg.dts_format)
        line = f"{'Document Generated': <20}: {dts}"
        p = Paragraph(line, bulletText=u'\u2022')
        self._elements.append(p)

    # -------------------
    def _gen_title(self, title):
        p = Paragraph(f'<b>{title}</b>', self._style_sheet['BodyText'])
        self._elements.append(p)
