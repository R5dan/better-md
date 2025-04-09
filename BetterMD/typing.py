import typing as t

ATTR_TYPES = t.Union[str, bool, int, float, list, dict]

ATTRS = t.Union[
  t.TypedDict("ATTRS", {
    "style": 'dict[str, ATTR_TYPES]',
    "class": 'list[str]'
}), 
  'dict[str, ATTR_TYPES]'
]
