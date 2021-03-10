# -*- coding: utf-8 -*-
from pathlib import Path
from users import User
from work_log import WorkLog
import shutil
import pickle
from datetime import datetime, timedelta, timezone


JST = timezone(timedelta(hours=+9), 'JST')


class Exercise:
    def __init__(self, user_data, ex_id):
        self._user_data = user_data
        self.ex_id = ex_id
        self.ex_dir = user_data.user_dir / ex_id
        self.works = {}
        self.time_stamp = None

    def setWorks(self, works):
        self.works = works

    def work(self, work_id):
        key = str(work_id)
        if not key in self.works.keys():
            self.works[key] = Work(self, work_id)
        return self.works[key]

    def greeting(self):
        print("{0}<{1}>さん，こんにちは！".format(
            self._user_data.user_name, self._user_data.user_id))
        print("{0}の課題を進めて行きましょう．".format(self.ex_id))

    def submitFiles(self):
        for task in self.works.values():
            task.submitFiles()

    def sessionFile(self, file_name):
        return Path("{0}{1}".format(self.ex_id, file_name))

    def driveFile(self, file_name):
        return self.ex_dir / self.sessionFile(file_name)

    def submit(self):
        self.submitFiles()


class Work:
    def __init__(self, ex_info, work_id):
        self._ex_info = ex_info

        self.work_id = work_id
        self.ex_id = ex_info.ex_id
        self.ex_dir = ex_info.ex_dir
        self._file_names = []
        self._data = {}
        self._work_log = WorkLog(self.ex_id, self.work_id,
                                 self._ex_info._user_data.user_id, self._ex_info._user_data.user_name)

    def log(self, *args, **kargs):
        files = [self.driveFile(file_name) for file_name in self._file_names]
        self._work_log.addFiles(files)
        self._work_log.log(*args, **kargs)

    def _debug(self):
        print(self._data.keys())

    def savefig(self, fig, file_name):
        self._file_names.append(file_name)
        fig.savefig(self.sessionFile(file_name), transparent=True,
                    bbox_inches='tight', pad_inches=0)

    def sessionFile(self, file_name):
        return Path("{0}-{1}{2}".format(self.ex_id, self.work_id, file_name))

    def driveFile(self, file_name):
        return self.ex_dir / self.sessionFile(file_name)

    def submitFiles(self):
        print("- {0}-{1}を更新しました．".format(self.ex_id, self.work_id))

        for file_name in self._file_names:
            src_file = self.sessionFile(file_name)
            if not src_file.exists():
                print("{0}: NG".format(str(src_file)))
                continue

            dst_file = self.driveFile(file_name)
            dst_dir = dst_file.parent

            if not dst_dir.exists():
                dst_dir.mkdir(parents=True)

            shutil.copy2(src_file, dst_file)

        log_file = self.driveFile(".log")
        self._work_log.save(log_file)


def loadExercise(ex_id):
    user_data = User()

    ex_info = Exercise(user_data, ex_id)

    ex_info.greeting()
    return ex_info
