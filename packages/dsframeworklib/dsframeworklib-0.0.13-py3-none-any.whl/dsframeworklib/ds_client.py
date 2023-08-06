from abc import ABCMeta, abstractmethod


class dClient(metaclass=ABCMeta):
    def __init__(self, host, port):
        self.addr = (host, port)

    @staticmethod
    def RequestHandler(**kwargs):
        pass


if __name__ == "__main__":
    pass
