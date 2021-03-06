# -*- coding: utf-8 -*-
import os
import shutil
import asyncio
import logging
import re

# from watchdog.observers import Observer
# from watchdog.events import PatternMatchingEventHandler, FileSystemEventHandler
logger = logging.getLogger('tailor.filesystem')

regex = re.compile('^(.*?)-(\d+)$')


class FileCopy:
    def __init__(self, dest, **kwargs):
        self.dest = dest
        self.overwrite = kwargs.get('overwrite', False)

    @asyncio.coroutine
    def process(self, filename):
        path = os.path.join(self.dest, os.path.basename(filename))

        root, ext = os.path.splitext(path)
        match = regex.match(root)
        if match:
            root, i = match.groups()
            i = int(i)
        else:
            i = 0

        if not self.overwrite and os.path.exists(path):
            i += 1
            path = "{0}-{1:04d}{2}".format(root, i, ext)
            while os.path.exists(path):
                i += 1
                path = "{0}-{1:04d}{2}".format(root, i, ext)

        loop = asyncio.get_event_loop()
        task = loop.run_in_executor(None, shutil.copyfile, filename, path)
        yield from task
        return path


class FileDelete:
    def process(self, msg):
        os.unlink(msg)

# class FileWatcher:
#     """
#     Simple watcher that uses a glob to track new files
#     This class will publish paths to new images
#     """
#
#     def __init__(self, path, regex=None, recursive=False):
#         self._path = path
#         self._regex = regex
#         self._recursive = recursive
#         self._queue = asyncio.Queue()
#         self._observer = None
#         self.handler = None
#
#     def reset(self):
#         if self._observer is not None:
#             self._observer.stop()
#
#         if self._regex is None:
#             self.handler = FileSystemEventHandler()
#         else:
#             self.handler = PatternMatchingEventHandler(self._regex)
#         self._observer = Observer()
#         self._observer.schedule(self.handler, self._path, self._recursive)
#         self._observer.start()
#         return self.handler
