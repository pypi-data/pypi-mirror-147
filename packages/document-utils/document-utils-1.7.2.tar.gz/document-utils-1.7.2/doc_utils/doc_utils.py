from copy import deepcopy

from typing import Dict, List, Any

from .chunk_doc_utils import ChunkDocUtils


class DocUtils(ChunkDocUtils):
    """Class for all document utilities.
    Primarily should be used as a mixin for future functions
    but can be a standalone.
    # TODO: Extend to Chunk Doc Reading and Chunk Doc Writing
    """


class Document(DocUtils):
    """
    A Class for handling json like arrays of dictionaries

    Example:
    >>> doc = Document({"value": 3"})
    >>> doc['value'] # returns 3
    >>> doc['value'] = 3 # should set the value
    """

    def __init__(self, document: Dict):
        super().__init__()

        for key, value in document.items():
            if isinstance(value, dict):
                document[key] = Document(value)

        self.data = deepcopy(document)

    def __repr__(self):
        return str(self.data)

    def __getitem__(self, key: str) -> Any:
        levels = key.split(".")

        value = self.data
        for level in levels:
            value = value.__getitem__(level)

        return value

    def __setitem__(self, key: str, value: Any) -> None:
        self.setitem(self, key.split("."), value)

    def setitem(self, obj, keys: List[str], value: Any) -> None:
        for key in keys[:-1]:
            obj = obj.data.setdefault(key, {})
        obj.data[keys[-1]] = value

    def json(self):
        document = {}
        for key, value in self.data.items():
            if isinstance(value, self.__class__):
                document[key] = value.json()
            else:
                document[key] = value
        return document


class DocumentList(DocUtils):
    """
    A Class for handling json like arrays of dictionaries

    Example:
    >>> docs = DocumentList([{"value": 2}, {"value": 10}])
    """

    def __init__(self, documents: List):
        super().__init__()

        self.documents = [Document(document) for document in documents]

    def __getitem__(self, index):
        return self.documents[index]

    def json(self):
        return [document.json() for document in self.documents]
