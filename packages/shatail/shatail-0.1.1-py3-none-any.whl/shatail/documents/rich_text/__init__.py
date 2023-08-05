from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import escape

from shatail.documents import get_document_model
from shatail.rich_text import LinkHandler

# Front-end conversion


class DocumentLinkHandler(LinkHandler):
    identifier = "document"

    @staticmethod
    def get_model():
        return get_document_model()

    @classmethod
    def expand_db_attributes(cls, attrs):
        try:
            doc = cls.get_instance(attrs)
            return '<a href="%s">' % escape(doc.url)
        except (ObjectDoesNotExist, KeyError):
            return "<a>"
