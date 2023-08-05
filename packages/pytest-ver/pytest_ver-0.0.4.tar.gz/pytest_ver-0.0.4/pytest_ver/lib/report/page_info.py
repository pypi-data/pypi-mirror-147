from pytest_ver.lib.report.footer import Footer
from pytest_ver.lib.report.header import Header
from pytest_ver.lib.report.page_details import PageDetails
from .. import services


# -------------------
class PageInfo:

    # -------------------
    def __init__(self):
        self.orientation = 'landscape'
        self.page_size = 'letter'
        self.header = Header()
        self.footer = Footer()

        self._tp_results = PageDetails()
        self._tp_results.orientation = 'landscape'

        self._trace = PageDetails()
        self._trace.orientation = 'landscape'

        self._summary = PageDetails()
        self._trace.orientation = 'portrait'

    # -------------------
    def __getitem__(self, item):
        if item == 'header':
            return self.header

        if item == 'footer':
            return self.footer

        if item == 'orientation':
            return self.orientation

        if item == 'page_size':
            return self.page_size

        services.logger.err(f'bad item name: {item}')
        services.harness.abort()

    # -------------------
    def init_tp_result(self, item):
        self._set_all_fields(item, self._tp_results)

    # -------------------
    def init_trace(self, item):
        self._set_all_fields(item, self._trace)

    # -------------------
    def init_summary(self, item):
        self._set_all_fields(item, self._summary)

    # -------------------
    def set_tp_cfg(self):
        self._set_all_cfg(self._tp_results)

    # -------------------
    def set_trace_cfg(self):
        self._set_all_cfg(self._trace)

    # -------------------
    def set_summary_cfg(self):
        self._set_all_cfg(self._summary)

    # -------------------
    def report(self, fp):
        fp.write(f"{'Header left': <20}: {self.header.left}\n")
        fp.write(f"{'Header middle': <20}: {self.header.middle}\n")
        fp.write(f"{'Header right': <20}: {self.header.right}\n")

        fp.write(f"{'Footer left': <20}: {self.footer.left}\n")
        fp.write(f"{'Footer middle': <20}: {self.footer.middle}\n")
        fp.write(f"{'Footer right': <20}: {self.footer.right}\n")

    # === Private

    # -------------------
    def _set_all_cfg(self, src):
        self.orientation = src.orientation
        self.page_size = src.page_size

        self.header.left = src.header.left
        self.header.middle = src.header.middle
        self.header.right = src.header.right

        self.footer.left = src.footer.left
        self.footer.middle = src.footer.middle
        self.footer.right = src.footer.right

    # -------------------
    def _set_all_fields(self, src, dst):
        self._set_field(src, dst, 'orientation')
        self._set_field(src, dst, 'page_size')
        self._set_sub_field(src, dst, 'header', 'left')
        self._set_sub_field(src, dst, 'header', 'middle')
        self._set_sub_field(src, dst, 'header', 'right')
        self._set_sub_field(src, dst, 'footer', 'left')
        self._set_sub_field(src, dst, 'footer', 'middle')
        self._set_sub_field(src, dst, 'footer', 'right')

    # -------------------
    def _set_field(self, src, dst, field):
        if field in src:
            dst[field] = src[field]

    # -------------------
    def _set_sub_field(self, src, dst, sub, field):
        if field in src[sub]:
            dst[sub][field] = src[sub][field]
