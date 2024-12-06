from io import BytesIO
from pathlib import Path
from typing import Iterable, Iterator

from docling.datamodel.base_models import DocumentStream, InputFormat
from docling.document_converter import ConversionResult, DocumentConverter, FormatOption
from docling_core.types.doc.base import CoordOrigin
from docling_core.types.doc.labels import DocItemLabel
from spacy.language import Language
from spacy.tokens import Doc, Span, SpanGroup

from .types import Attrs, DocLayout, PageLayout, SpanLayout


class spaCyLayout:
    def __init__(
        self,
        nlp: Language,
        separator: str | None = "\n\n",
        attrs: dict[str, str] = {},
        headings: list[str] = [
            DocItemLabel.SECTION_HEADER,
            DocItemLabel.PAGE_HEADER,
            DocItemLabel.TITLE,
        ],
        docling_options: dict[InputFormat, FormatOption] | None = None,
    ) -> None:
        """Initialize the layout parser and Docling converter."""
        self.nlp = nlp
        self.sep = separator
        self.attrs = Attrs(
            doc_layout=attrs.get("doc_layout", "layout"),
            doc_pages=attrs.get("doc_pages", "pages"),
            span_layout=attrs.get("span_layout", "layout"),
            span_heading=attrs.get("span_heading", "heading"),
            span_group=attrs.get("span_group", "layout"),
        )
        self.headings = headings
        self.converter = DocumentConverter(format_options=docling_options)
        # Set spaCy extension attributes for custom data
        Doc.set_extension(self.attrs.doc_layout, default=None, force=True)
        Doc.set_extension(self.attrs.doc_pages, getter=self.get_pages, force=True)
        Span.set_extension(self.attrs.span_layout, default=None, force=True)
        Span.set_extension(self.attrs.span_heading, getter=self.get_heading, force=True)

    def __call__(self, source: str | Path | bytes) -> Doc:
        """Call parser on a path to create a spaCy Doc object."""
        result = self.converter.convert(self._get_source(source))
        return self._result_to_doc(result)

    def pipe(self, sources: Iterable[str | Path | bytes]) -> Iterator[Doc]:
        """Process multiple documents and create spaCy Doc objects."""
        data = (self._get_source(source) for source in sources)
        results = self.converter.convert_all(data)
        for result in results:
            yield self._result_to_doc(result)

    def _get_source(self, source: str | Path | bytes) -> str | Path | DocumentStream:
        if isinstance(source, (str, Path)):
            return source
        return DocumentStream(name="source", stream=BytesIO(source))

    def _result_to_doc(self, result: ConversionResult) -> Doc:
        inputs = []
        pages = {
            (page.page_no + 1): PageLayout(
                page_no=page.page_no + 1,
                width=page.size.width if page.size else 0,
                height=page.size.height if page.size else 0,
            )
            for page in result.pages
        }
        for item in result.document.texts:
            if item.text == "":
                continue
            bounding_box = None
            if item.prov:
                prov = item.prov[0]
                page = pages[prov.page_no]
                if page.width and page.height:
                    is_bottom = prov.bbox.coord_origin == CoordOrigin.BOTTOMLEFT
                    y = page.height - prov.bbox.t if is_bottom else prov.bbox.t
                    height = prov.bbox.t - prov.bbox.b if is_bottom else prov.bbox.t
                    bounding_box = SpanLayout(
                        x=prov.bbox.l,
                        y=y,
                        width=prov.bbox.r - prov.bbox.l,
                        height=height,
                        page_no=prov.page_no,
                    )
            inputs.append((item.text, item.label, bounding_box))
        doc = self._texts_to_doc(inputs)
        doc._.set(self.attrs.doc_layout, DocLayout(pages=[p for p in pages.values()]))
        return doc

    def _texts_to_doc(self, inputs: list[tuple[str, str, SpanLayout]]) -> Doc:
        """Convert Docling structure to spaCy Doc."""
        words = []
        spaces = []
        span_data = []
        token_idx = 0
        data = ((item_text, (label, layout)) for item_text, label, layout in inputs)
        # Tokenize the span because we can't rely on the document parsing to
        # give us items that are not split across token boundaries
        with self.nlp.select_pipes(disable=self.nlp.pipe_names):
            for span_doc, (label, layout) in self.nlp.pipe(data, as_tuples=True):
                words += [token.text for token in span_doc]
                spaces += [bool(token.whitespace_) for token in span_doc]
                # Add separator token and don't include it in the layout span
                if self.sep:
                    words.append(self.sep)
                    spaces[-1] = False
                    spaces.append(False)
                end = token_idx + len(span_doc)
                span_data.append((token_idx, end, label, layout))
                token_idx += len(span_doc) + (1 if self.sep else 0)
        doc = Doc(self.nlp.vocab, words=words, spaces=spaces)
        spans = []
        for i, (start, end, label, layout) in enumerate(span_data):
            span = Span(doc, start=start, end=end, label=label, span_id=i)
            span._.set(self.attrs.span_layout, layout)
            spans.append(span)
        doc.spans[self.attrs.span_group] = SpanGroup(
            doc, name=self.attrs.span_group, spans=spans
        )
        return doc

    def get_pages(self, doc: Doc) -> list[tuple[PageLayout, list[Span]]]:
        """Get all pages and their layout spans."""
        layout = doc._.get(self.attrs.doc_layout)
        pages = {page.page_no: page for page in layout.pages}
        page_spans = {page.page_no: [] for page in layout.pages}
        for span in doc.spans[self.attrs.span_group]:
            span_layout = span._.get(self.attrs.span_layout)
            page_spans[span_layout.page_no].append(span)
        return [(pages[i], page_spans[i]) for i in page_spans]

    def get_heading(self, span: Span) -> Span | None:
        """Get the closest heading for a span."""
        spans = list(span.doc.spans[self.attrs.span_group])
        if span.label_ not in self.headings:
            # Go through previous layout spans in reverse and find first match
            for candidate in spans[: span.id][::-1]:
                if candidate.label_ in self.headings:
                    return candidate
