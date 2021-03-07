# -*- coding: utf-8 -*-
import pickle
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), 'JST')


class WorkLog:
    def __init__(self, ex_id, work_id, user_id, user_name):
        self.time_stamp = None
        self.ex_id = ex_id
        self.work_id = work_id
        self.user_id = user_id
        self.user_name = user_name

        self.files = []
        self.data = {}

    def log(self, *args, **kargs):
        self.time_stamp = datetime.now(JST)
        self.data = kargs

    def addFiles(self, files):
        self.files.extend(files)

    def save(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)
