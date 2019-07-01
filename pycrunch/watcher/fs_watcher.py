import threading
from pathlib import Path

from watchgod import watch

from pycrunch.pipeline import execution_pipeline
from pycrunch.pipeline.file_modification_task import FileModifiedNotificationTask
from ._abstract_watcher import Watcher

import logging

logger = logging.getLogger(__name__)


class FSWatcher(Watcher):
    def __init__(self):
        self.thread_lock = threading.Lock()
        self.thread = None
        self.files = []

    def thread_proc(self):
        logger.debug('thread_proc')
        logger.debug(f'files {self.files}')

        logger.debug(f'files {self.files}')

        path = Path('.').absolute()
        print('watching this:...')
        print(path)
        for changes in watch(path):
            for c in changes:
                file = c[1]
                if self.should_watch(file):
                    execution_pipeline.add_task(FileModifiedNotificationTask(file=file))
                    logger.info('Added file for pipeline ' + file)
                else:
                    logger.debug('non-significant file changed ' + file)

        logger.debug('END thread_proc')



    def watch(self, files):
        logger.debug('watch...')
        self.files = files
        with self.thread_lock:
            if self.thread is None:
                logger.info('Starting watch thread...')
                self.thread = threading.Thread(target=self.thread_proc)
                self.thread.start()

    def should_watch(self, file):
        return file in self.files

