
from logging import FileHandler
import multiprocessing
import threading
import logging
import sys
import traceback


class MultiProcessingLog(logging.Handler):
    def __init__(self, name):
        logging.Handler.__init__(self)

        self._handler = FileHandler(name)
        self.queue = multiprocessing.Queue(-1)

        t = threading.Thread(target=self.receive)
        t.daemon = True
        t.start()

    def setFormatter(self, fmt):
        logging.Handler.setFormatter(self, fmt)
        self._handler.setFormatter(fmt)

    def receive(self):
        while True:
            try:
                record = self.queue.get()
                self._handler.emit(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except:
                traceback.print_exc(file=sys.stderr)

    def send(self, s):
        self.queue.put_nowait(s)

    def _format_record(self, record):
        # ensure that exc_info and args
        # have been stringified.  Removes any chance of
        # unpickleable things inside and possibly reduces
        # message size sent over the pipe
        if record.args:
            record.msg = record.msg % record.args
            record.args = None
        if record.exc_info:
            dummy = self.format(record)
            record.exc_info = None

        return record

    def emit(self, record):
        try:
            s = self._format_record(record)
            self.send(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        self._handler.close()
        logging.Handler.close(self)


def init_logger(logger_name):
    logging_time_format = '%d-%m-%Y_%H:%M:%S'
    logging_message_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logfile_name = "my.log"

    logging_formatter = logging.Formatter(logging_message_format, logging_time_format)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    handler = MultiProcessingLog(logfile_name)
    handler.setFormatter(logging_formatter)
    logger.addHandler(handler)
    return logger
