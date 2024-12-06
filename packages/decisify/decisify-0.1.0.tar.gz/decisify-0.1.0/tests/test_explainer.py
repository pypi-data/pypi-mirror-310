from abc import ABC
from decisify.explainer import Interrogator
import pytest

class MockInterrogator(Interrogator):
    def answer(self, query: str):
        return f"Answering query: {query}"

    def explain(self, query: str):
        return f"Explaining decision for query: {query}"

    def what_if(self, query: str):
        return f"Analyzing what-if scenario for query: {query}"


def test_mock_interrogator_instantiation():
    """Test that a concrete subclass of Interrogator can be instantiated."""
    interrogator = MockInterrogator()
    assert isinstance(interrogator, Interrogator)

def test_answer_method():
    """Test the answer method of the MockInterrogator."""
    interrogator = MockInterrogator()
    query = "Why was the decision made?"
    response = interrogator.answer(query)
    assert response == f"Answering query: {query}"

def test_explain_method():
    """Test the explain method of the MockInterrogator."""
    interrogator = MockInterrogator()
    query = "How was the decision made?"
    response = interrogator.explain(query)
    assert response == f"Explaining decision for query: {query}"

def test_what_if_method():
    """Test the what-if method of the MockInterrogator."""
    interrogator = MockInterrogator()
    query = "What if the input was different?"
    response = interrogator.what_if(query)
    assert response == f"Analyzing what-if scenario for query: {query}"

def test_cannot_instantiate_abstract_class():
    """Test that the abstract Interrogator class cannot be instantiated."""
    with pytest.raises(TypeError):
        _ = Interrogator()





