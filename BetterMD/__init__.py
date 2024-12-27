import logging
from .elements import A, H1, H2, H3, H4, H5, H6, Head, OL, UL, LI, Text, Div, P, Span, Img, B, I, Br, Blockquote, Hr, Table, Tr, Td, Th, THead, TBody, Input, Code
from .html import CustomHTML
from .markdown import CustomMarkdown
from .rst import CustomRst


def enable_debug_mode():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("BetterMD")
