import typing as t

ATTR_TYPES = t.Union[str, bool, int, float, list['ATTR_TYPES'], dict[str, 'ATTR_TYPES']]

ATTRS = t.Union[
  t.TypedDict("ATTRS", {
    "style": 'dict[str, ATTR_TYPES]',
    "class": 'list[str]'
}), 
  'dict[str, ATTR_TYPES]'
]
