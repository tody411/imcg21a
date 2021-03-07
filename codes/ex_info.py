# -*- coding: utf-8 -*-
from pathlib import Path
from user import User
import shutil
import pickle
from datetime import datetime, timedelta, timezone


JST = timezone(timedelta(hours=+9), 'JST')


class ExInfo:
    def __init__(self, user_data, ex_id):
        self._user_data = user_data
        self.ex_id = ex_id
        self.ex_dir = user_data.user_dir / ex_id
        self.tasks = {}
        self.time_stamp = None

    def setTasks(self, tasks):
        self.tasks = tasks

    def task(self, task_id):
        key = str(task_id)
        if not key in self.tasks.keys():
            self.tasks[key] = ExTask(self, task_id)
        return self.tasks[key]

    def greeting(self):
        print("{0}<{1}>さん，こんにちは！".format(
            self._user_data.user_name, self._user_data.user_id))
        print("{0}の課題を進めて行きましょう．".format(self.ex_id))

    def submitFiles(self):
        for task in self.tasks.values():
            task.submitFiles()

    def sessionFile(self, file_name):
        return Path("{0}{1}".format(self.ex_id, file_name))

    def driveFile(self, file_name):
        return self.ex_dir / self.sessionFile(file_name)

    def submit(self):
        self.submitFiles()


class ExTask:
    def __init__(self, ex_info, task_id):
        self._ex_info = ex_info

        self.task_id = task_id
        self.ex_id = ex_info.ex_id
        self.ex_dir = ex_info.ex_dir
        self._file_names = []
        self._data = {}
        self._log_data = {}

    def logData(self):
        files = [self.driveFile(file_name) for file_name in self._file_names]
        return {"time_stamp": datetime.now(JST),
                "ex_id": self.ex_id, "task_id": self.task_id,
                "user_id": self._ex_info._user_data.user_id, "user_name": self._ex_info._user_data.user_name,
                "files": files, "data": self._data}

    def log(self, *args, **kargs):
        self._data = kargs
        self._log_data = self.logData()

    def _debug(self):
        print(self._data.keys())

    def savefig(self, fig, file_name):
        self._file_names.append(file_name)
        fig.savefig(self.sessionFile(file_name), transparent=True,
                    bbox_inches='tight', pad_inches=0)

    def sessionFile(self, file_name):
        return Path("{0}-{1}{2}".format(self.ex_id, self.task_id, file_name))

    def driveFile(self, file_name):
        return self.ex_dir / self.sessionFile(file_name)

    def submitFiles(self):
        print("- {0}-{1}を更新しました．".format(self.ex_id, self.task_id))

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

        with open(self.driveFile(".log"), 'wb') as f:
            pickle.dump(self._log_data, f)


def loadExInfo(ex_id):
    user_data = User()

    ex_info = ExInfo(user_data, ex_id)

    ex_info.greeting()
    return ex_info
