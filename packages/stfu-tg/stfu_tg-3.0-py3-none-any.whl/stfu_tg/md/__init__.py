from stfu_tg.doc import Element
from stfu_tg.md.misc import HRuler
from stfu_tg.md.table import TableMD


class MDOnlyElement(Element):
    def to_html(self):
        raise ValueError("This element does not support HTML type!")


__all__ = [
    'MDOnlyElement',
    'TableMD',
    'HRuler',
]
