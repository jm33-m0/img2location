# pylint: disable=invalid-name,missing-docstring

from __future__ import print_function

import os

import pandas as pd


class Database:

    def __init__(self, db_dir, db_csv):
        self.db_dir = db_dir
        self.db_csv = db_csv
        self._gen_csv()
        self.data = pd.read_csv(self.db_csv)
        self.classes = set(self.data["cls"])

    def _gen_csv(self):
        if os.path.exists(self.db_csv):
            return
        with open(self.db_csv, 'w', encoding='UTF-8') as f:
            f.write("img,cls")

            for root, _, files in os.walk(self.db_dir, topdown=False):
                cls = root.split('/')[-1]

                for name in files:
                    if not name.endswith('.jpg'):
                        continue
                    img = os.path.join(root, name)
                    f.write("\n{},{}".format(img, cls))

    def __len__(self):
        return len(self.data)

    def get_class(self):
        return self.classes

    def get_data(self):
        return self.data


def main():
    db = Database("database", "data.csv")
    data = db.get_data()
    print(data)
    classes = db.get_class()

    print("DB length:", len(db))
    print(classes)
