from pathlib import Path

import pytest
import spacy
from docling_core.types.doc.labels import DocItemLabel

from spacy_layout import spaCyLayout
from spacy_layout.types import DocLayout, SpanLayout

PDF_STARCRAFT = Path(__file__).parent / "data" / "starcraft.pdf"
PDF_SIMPLE = Path(__file__).parent / "data" / "simple.pdf"
DOCX_SIMPLE = Path(__file__).parent / "data" / "simple.docx"
PDF_SIMPLE_BYTES = PDF_SIMPLE.open("rb").read()


@pytest.fixture
def nlp():
    return spacy.blank("en")


@pytest.fixture
def span_labels():
    return [label.value for label in DocItemLabel]


@pytest.mark.parametrize("path", [PDF_STARCRAFT, PDF_SIMPLE, PDF_SIMPLE_BYTES])
def test_general(path, nlp, span_labels):
    layout = spaCyLayout(nlp)
    doc = layout(path)
    assert isinstance(doc._.get(layout.attrs.doc_layout), DocLayout)
    for span in doc.spans[layout.attrs.span_group]:
        assert span.text
        assert span.label_ in span_labels
        assert isinstance(span._.get(layout.attrs.span_layout), SpanLayout)


@pytest.mark.parametrize("path", [PDF_SIMPLE, DOCX_SIMPLE])
@pytest.mark.parametrize("separator", ["\n\n", ""])
def test_simple(path, separator, nlp):
    layout = spaCyLayout(nlp, separator=separator)
    doc = layout(path)
    assert len(doc.spans[layout.attrs.span_group]) == 4
    assert doc.text.startswith(f"Lorem ipsum dolor sit amet{separator}")
    assert doc.spans[layout.attrs.span_group][0].text == "Lorem ipsum dolor sit amet"


def test_simple_pipe(nlp):
    layout = spaCyLayout(nlp)
    for doc in layout.pipe([PDF_SIMPLE, DOCX_SIMPLE]):
        assert len(doc.spans[layout.attrs.span_group]) == 4
