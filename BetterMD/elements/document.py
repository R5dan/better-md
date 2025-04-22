import typing as t

if t.TYPE_CHECKING:
    from .symbol import Symbol
    from ..typing import ATTR_TYPES

T1 = t.TypeVar("T1")
T2 = t.TypeVar("T2")
T3 = t.TypeVar("T3")
T4 = t.TypeVar("T4")

ARGS = t.ParamSpec("ARGS")

class HashableList(t.Generic[T1]):
    def __init__(self, lst:'list[T1]'):
        self.lst = lst

    def __hash__(self):
        # Convert list to tuple for hashing
        return hash(tuple(self.lst))

    def __eq__(self, other):
        if not isinstance(other, HashableList):
            return False
        return self.lst == other.lst

    def __repr__(self):
        return f"HashableList({self.lst})"


class HashableDict(t.Generic[T1, T2]):
    def __init__(self, dct:'dict[T1, T2]'):
        self.dct = dct

    def __hash__(self):
        # Convert list to tuple for hashing
        return hash(tuple(self.dct.items()))

    def __eq__(self, other):
        if not isinstance(other, HashableDict):
            return False
        return self.dct == other.dct

    def __repr__(self):
        return f"HashableList({self.dct})"


class GetProtocol(t.Protocol, t.Generic[T1, T2]):
    def get(self, key: 'T1', ) -> 'T2': ...

@t.runtime_checkable
class CopyProtocol(t.Protocol, t.Generic[T1]):
    def copy(self) -> 'T1': ...

class Copy:
    def __init__(self, data):
        self.data = data

    def copy(self):
        return self.data

T5 = t.TypeVar("T5", bound=CopyProtocol)
HASHABLE_ATTRS = str | bool | int | float | HashableList['HASHABLE_ATTRS'] | HashableDict[str, 'HASHABLE_ATTRS']

class Fetcher(t.Generic[T1, T2, T5]):
    def __init__(self, data: 't.Union[GetProtocol[T1, T2], dict[T1, T2]]', default:'T5'=Copy(None)):
        self.data = data
        self.default = default.copy() if isinstance(default, CopyProtocol) else default

    def __getitem__(self, name:'T1') -> 'T2|T5':
        if isinstance(self.data, dict):
            return self.data.get(name, self.default)
        return self.data.get(name, self.default)
class InnerHTML:
    def __init__(self, inner):
        self.inner = inner

        self.ids: 'dict[str|None, list[Symbol]]' = {}
        self.classes: 'dict[str, list[Symbol]]' = {}
        self.tags: 'dict[type[Symbol], list[Symbol]]' = {}
        self.attrs: 'dict[str, dict[HASHABLE_ATTRS, list[Symbol]]]' = {}
        self.text: 'dict[str, list[Symbol]]' = {}

        self.children_ids: 'dict[str|None, list[Symbol]]' = {}
        self.children_classes: 'dict[str, list[Symbol]]' = {}
        self.children_tags: 'dict[type[Symbol], list[Symbol]]' = {}
        self.children_attrs: 'dict[str, dict[str, list[Symbol]]]' = {}
        self.children_text: 'dict[str, list[Symbol]]' = {}

    def add_elm(self, elm: 'Symbol'):
        def make_hashable(v):
            if isinstance(v, list):
                return HashableList(v)
            elif isinstance(v, dict):
                return HashableDict(v)
            return v

        self.children_ids.setdefault(elm.get_prop("id", None), []).append(elm)
        [self.children_classes.setdefault(c, []).append(elm) for c in elm.classes]
        self.children_tags.setdefault(type(elm), []).append(elm)

        # Normalize keys when adding to children_attrs
        for prop, value in elm.props.items():
            key = make_hashable(value)
            self.children_attrs.setdefault(prop, {}).setdefault(key, []).append(elm)

        self.children_text.setdefault(elm.text, []).append(elm)

        def concat(d1: 'dict', *d2: 'dict'):
            ret = {}

            for dict_ in list(d2) + [d1]:
                for k, v in dict_.items():
                    ret.setdefault(k, []).extend(v)

            return ret

        # Normalize keys in elm.props for attrs merging
        normalized_props = {
            prop: {make_hashable(value): [elm] for value in values}
            for prop, values in elm.props.items()
        }

        self.ids = concat(self.ids, elm.inner_html.ids, {elm.get_prop("id", None): [elm]})
        self.classes = concat(self.classes, elm.inner_html.classes, {c: [elm] for c in elm.classes})
        self.tags = concat(self.tags, elm.inner_html.tags, {type(elm): [elm]})
        self.attrs = concat(self.attrs, elm.inner_html.attrs, normalized_props)
        self.text = concat(self.text, elm.inner_html.text, {elm.text: [elm]})

    def get_elements_by_id(self, id: 'str'):
        return self.ids.get(id, [])

    def get_elements_by_class_name(self, class_name: 'str'):
        return self.classes.get(class_name, [])

    def get_elements_by_tag_name(self, tag: 'str'):
        # Find the tag class by name
        for tag_class, elements in self.tags.items():
            if tag_class.__name__.lower() == tag.lower():
                return elements
        return []

    def find(self, key:'str'):
        if key.startswith("#"):
            return self.get_elements_by_id(key[1:])
        elif key.startswith("."):
            return self.get_elements_by_class_name(key[1:])
        else:
            return self.get_elements_by_tag_name(key)

    def get_by_text(self, text:'str'):
        return self.text.get(text, [])

    def get_by_attr(self, attr:'str', value:'str'):
        return self.attrs.get(attr, {}).get(value, [])

    def advanced_find(self, tag:'str', attrs:'dict[t.Literal["text"] | str, str | bool | int | float | tuple[str, str | bool | int | float] | list[str | bool | int | float | tuple[str, str | bool | int | float]]]' = {}):
        def check_attr(e:'Symbol', k:'str', v:'str | bool | int | float | tuple[str, str | bool | int | float]'):
            prop = e.get_prop(k)
            if isinstance(prop, list):
                return v in prop

            if isinstance(prop, dict):
                return v in list(prop.items())

            return prop == v

        tags = self.find(tag)
        if "text" in attrs:
            text = attrs.pop("text")
            tags = filter(lambda e: e.text == text, tags)

        for k, v in attrs.items():
            tags = filter(lambda e: check_attr(e, k, v) if not isinstance(v, list) else all([check_attr(e, k, i) for i in v]), tags)
        return list(tags)

    @property
    def id(self):
        return Fetcher(self.children_ids, [])

    @property
    def cls(self):
        return Fetcher(self.children_classes, [])

    @property
    def tag(self):
        return Fetcher(self.children_tags, [])