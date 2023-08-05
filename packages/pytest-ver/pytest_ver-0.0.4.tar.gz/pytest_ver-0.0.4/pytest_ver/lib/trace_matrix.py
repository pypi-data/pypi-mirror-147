from . import services


# -------------------
class TraceMatrix:
    # -------------------
    def __init__(self):
        self._matrix = {}

    # -------------------
    def term(self):
        self.save()

    # -------------------
    def add_proto(self, req_ids, proto_id, proto_info):
        for req_id in req_ids:
            if req_id in self._matrix:
                self._add_to(req_id, proto_id, proto_info)
            else:
                self._add(req_id, proto_id, proto_info)
        self.save()

    # -------------------
    def _add(self, req_id, proto_id, proto_info):
        self._matrix[req_id] = [
            {
                'proto_id': proto_id,
                'proto_info': proto_info,  # TODO what info?
            }
        ]

    # -------------------
    def _add_to(self, req_id, proto_id, proto_info):
        self._matrix[req_id].append(
            {
                'proto_id': proto_id,
                'proto_info': proto_info,  # TODO what info?
            }
        )

    # -------------------
    def save(self):
        services.storage.save_trace(self._matrix)
