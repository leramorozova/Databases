import json

import pandas as pd

from pymongo import MongoClient
from typing import Dict


class DBClient:
    """
    Класс для инициализации базы данных.
    """
    def __init__(self):
        self._client = MongoClient()
        self._db = self._client.DataBase
        self._db.indirect_questions.drop()

        self.data = self._db.indirect_questions

        self._append_dummy_data()

    def _append_dummy_data(self):
        """
        Метод подгружает стартовые данные для базы (чтобы при запуске приложения она не была пустой)
        """
        with open("pre_data.json", "r") as fd:
            question_markers = json.load(fd)
        self.data.insert_many(question_markers)

    def serialize_data(self, param=None):
        pd_data = dict()
        for doc in self.data.find(param):
            for key in doc:
                value = ", ".join(doc[key]) if isinstance(doc[key], list) else doc[key]
                if key in ["_id"]:
                    continue
                elif key in pd_data:
                    pd_data[key].append(value)
                else:
                    pd_data[key] = [value]
        df = pd.DataFrame(data=pd_data)
        return df.to_html(classes="table table-hover")


class FormHandler:
    _QUESTION_TYPES = ["polar", "wh", "alternative"]
    _POLYSEMY = ["adverbial clause", "concessive clause", "conditional mood", "relative clause", "modality marker",
                 "complement clause"]
    _FIELDS = ["lang", "genetics", "geography", "construction", "question types", "subordinator", "question word",
               "quotative", "comment", "polysemy"]

    @staticmethod
    def compile_query(req_data: Dict) -> Dict:
        query = {}
        for key in req_data:
            if req_data[key] and key not in FormHandler._POLYSEMY and key not in FormHandler._QUESTION_TYPES:
                query[key] = req_data[key]

            elif key in FormHandler._QUESTION_TYPES:
                if "question types" not in query:
                    query["question types"] = [req_data[key]]
                else:
                    query["question types"].append(req_data[key])

            elif key in FormHandler._POLYSEMY:
                if "polysemy" not in query:
                    query["polysemy"] = [req_data[key]]
                else:
                    query["polysemy"].append(req_data[key])
        return query

    @staticmethod
    def update_query(query_data: Dict):
        for field in FormHandler._FIELDS:
            if field not in query_data:
                query_data[field] = ""
