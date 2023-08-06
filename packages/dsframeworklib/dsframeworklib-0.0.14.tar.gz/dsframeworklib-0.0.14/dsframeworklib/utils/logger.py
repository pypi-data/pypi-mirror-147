import logging

logging.basicConfig(level=logging.INFO)


class Logger(object):
    def __init__(self, **kwargs):
        self.debug_log = logging.getLogger()
        self.info_log = logging.getLogger()

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        if('debug_file' in kwargs):
            dfh = logging.FileHandler(kwargs['debug_file'])
            dfh.setLevel(logging.DEBUG)
            dfh.setFormatter(formatter)
            self.debug_log.addHandler(dfh)
        else:
            dch = logging.StreamHandler()
            dch.setLevel(logging.DEBUG)
            dch.setFormatter(formatter)
            self.debug_log.addHandler(dch)

        if('info_file' in kwargs):
            ifh = logging.FileHandler(kwargs['info_file'])
            ifh.setLevel(logging.INFO)
            ifh.setFormatter(formatter)
            self.info_log.addHandler(ifh)
        else:
            ich = logging.StreamHandler()
            ich.setLevel(logging.INFO)
            ich.setFormatter(formatter)
            # self.info_log.addHandler(ich)

    def fdebug(self, stream: str):
        self.debug_log.debug(stream)

    def finfo(self, stream: str):
        self.info_log.info(stream)
