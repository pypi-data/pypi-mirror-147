from abc import ABC, abstractmethod

from .. import services


# -------------------
class Storage(ABC):
    # -------------------
    @classmethod
    def factory(cls):
        if services.cfg.storage_type == 'dev':
            from .storage_dev import StorageDev
            return StorageDev()
        else:
            services.logger.err(f'unknown Storage stype: {services.cfg.storage_type}')
            services.harness.abort()

    # -------------------
    @abstractmethod
    def term(self):
        pass

    # -------------------
    @abstractmethod
    def save_protocol(self, protocols):
        pass

    # -------------------
    @abstractmethod
    def get_protocols(self):
        pass

    # -------------------
    @abstractmethod
    def save_trace(self, trace):
        pass

    # -------------------
    @abstractmethod
    def get_trace(self):
        pass

    # -------------------
    @abstractmethod
    def save_summary(self, summary):
        pass

    # -------------------
    @abstractmethod
    def get_summary(self):
        pass
