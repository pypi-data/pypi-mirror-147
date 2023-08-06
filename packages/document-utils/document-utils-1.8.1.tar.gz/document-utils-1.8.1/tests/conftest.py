import pytest
import random


@pytest.fixture
def sample_document():
    return {"value": 100, "blast32": 21}


@pytest.fixture
def sample_nested_document():
    return {"value1": {"value2": {"value3": 100}}, "blast32": 21}


@pytest.fixture
def sample_2_document():
    return {"check_value": random.randint(0, 100)}


@pytest.fixture
def combined_sample_document():
    return {
        "value": random.randint(0, 99999),
        "check_value": random.randint(0, 9999999),
    }


@pytest.fixture
def sample_3_document():
    return {"check": random.randint(0, 100)}


@pytest.fixture
def sample_documents(sample_document, sample_nested_document):
    documents = [sample_document] * 50 + [sample_nested_document] * 50
    random.shuffle(documents)
    return documents
