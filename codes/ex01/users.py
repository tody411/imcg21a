# -*- coding: utf-8 -*-
from pathlib import Path
import json

root_dir = Path("/content/drive/My Drive/imcg/imcg21a")


def loadUserProfile():
    if not root_dir.exists():
        root_dir.mkdir(parents=True)

    with open(str(root_dir/'user.json'), mode='rt', encoding='utf-8') as file:
        data = json.load(file)
    return data


def saveUserProfile(data):
    user_dir = root_dir / "users" / data["user_id"]
    # 設定情報を演習フォルダのルートに配置: 再度読み込んだ際にアクセス可能
    # - Google Drive上のパス: imcg/imcg21a/user.json
    with open(str(root_dir/'user.json'), mode='wt', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    # 設定情報を個人フォルダのルートに配置: 再度読み込んだ際にアクセス可能
    # - Google Drive上のパス: imcg/imcg21a/users/[user_id]/user.json
    with open(str(user_dir/'user.json'), mode='wt', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


class User:
    def __init__(self, user_id=None):
        if user_id is not None:
            self.user_id = user_id
            self.user_dir = root_dir / "users" / self.user_id

        else:
            self._data = loadUserProfile()
            self.user_id = self._data["user_id"]
            self.user_name = self._data["user_name"]
            self.user_dir = root_dir / "users" / self.user_id


def loadUserInfo():
    user_data = User()
    return user_data
