from collections.abc import MutableSequence

from typing import Dict, List, Any

from .chunk_doc_utils import ChunkDocUtils

try:
    from IPython.display import display
except ModuleNotFoundError:
    pass


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

        self.data = document

    def _ipython_display_(self):
        display(self.json())

    def __repr__(self):
        return str(self.json())

    def __len__(self):
        return len(self.json())

    def __eq__(self, other):
        try:
            for key1, key2, value1, value2 in zip(
                self.keys(),
                other.keys(),
                self.values(),
                other.values(),
            ):
                if value1 != value2:
                    return False
            return True
        except:
            return False

    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError
        if hasattr(self, "data"):
            if name in self.data:
                return self.data[name]
        raise AttributeError

    def __getitem__(self, key: str) -> Any:
        levels = key.split(".")

        value = self.data
        for level in levels:
            value = value.__getitem__(level)

        return value

    def __iter__(self):
        return iter(self.keys())

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

    def keys(self, parent=None):
        keys = {}

        for key, value in self.data.items():
            if isinstance(value, self.__class__):
                if parent is not None:
                    subparent = f"{parent}.{key}"
                else:
                    subparent = key
                keys.update({key: None for key in value.keys(parent=subparent)})
                keys.update({subparent: None})
            else:
                if parent is None:
                    keys[key] = None
                else:
                    keys[f"{parent}.{key}"] = None

        return keys.keys()

    def values(self):
        values = {i: self[key] for i, key in enumerate(self.keys())}
        return values.values()

    def items(self):
        items = {
            key: value for key, value in zip(list(self.keys()), list(self.values()))
        }
        return items.items()

    def update(self, other: Dict[str, Any]):
        for key, value in other.items():
            if isinstance(value, dict):
                self.data[key] = Document(value)
            else:
                self.data[key] = value


class DocumentList(DocUtils, MutableSequence):
    """
    A Class for handling json like arrays of dictionaries

    Example:
    >>> docs = DocumentList([{"value": 2}, {"value": 10}])
    """

    def __init__(self, documents: List):
        super().__init__()

        self.documents = [
            Document(document) if not isinstance(document, Document) else document
            for document in documents
        ]

    def _ipython_display_(self):
        display(self.json())

    def __repr__(self):
        return repr([document.json() for document in self.documents])

    def __len__(self):
        return len(self.documents)

    def __add__(self, other):
        self.documents += other.documents
        return self

    def __contains__(self, document):
        return document in self.documents

    def __getitem__(self, index):
        return self.documents[index]

    def __setitem__(self, index, document):
        if isinstance(document, dict):
            document = Document(document)
        assert isinstance(document, Document)
        self.documents[index] = document

    def __delitem__(self, index):
        del self.documents[index]

    def insert(self, index, document):
        if isinstance(document, dict):
            document = Document(document)
        assert isinstance(document, Document)
        self.documents.insert(index, document)

    def json(self):
        return [document.json() for document in self.documents]
