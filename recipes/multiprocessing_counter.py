# -*- coding: utf-8 -*-

from multiprocessing import Value


class MultiprocessingCounter(object):
    """ Instance of this class can be shared
    safely between threads and between processes """

    def __init__(self):
        self.val = Value('i', 0)

    def increment(self, n=1):
        with self.val.get_lock():
            self.val.value += n

    @property
    def value(self):
        return self.val.value
