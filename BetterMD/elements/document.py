import typing as t

if t.TYPE_CHECKING:
    from .symbol import Symbol

T1 = t.TypeVar("T1")
T2 = t.TypeVar("T2")
T3 = t.TypeVar("T3")
T4 = t.TypeVar("T4")

ARGS = t.ParamSpec("ARGS")

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

class Fetcher(t.Generic[T1, T2, T5]):
    def __init__(self, data: 'GetProtocol[T1, T2]', default:'T5'=Copy(None)):
        self.data = data
        self.default = default.copy() if isinstance(default, CopyProtocol) else default

    def __getitem__(self, name:'T1') -> 'T2|T5':
        return self.data.get(name, self.default)
class InnerHTML:
    def __init__(self, inner):
        self.inner = inner

        self.ids: 'dict[str|None, list[Symbol]]' = {}
        self.classes: 'dict[str, list[Symbol]]' = {}
        self.tags: 'dict[type[Symbol], list[Symbol]]' = {}

        self.children_ids: 'dict[str|None, list[Symbol]]' = {}
        self.children_classes: 'dict[str, list[Symbol]]' = {}
        self.children_tags: 'dict[type[Symbol], list[Symbol]]' = {}

    def add_elm(self, elm:'Symbol'):
        """
        Add an element to the children indexes and merge the element's own indexes
        recursively into aggregate indexes.

        Args:
            elm: Symbol element to add to the indexes.
        """
        self.children_ids.setdefault(elm.get_prop("id", None), []).append(elm)
        [self.children_classes.setdefault(c, []).append(elm) for c in elm.classes]
        self.children_tags.setdefault(type(elm), []).append(elm)

        def concat(d1: 'dict[T1|T3, list[T2|T4]]', *d2: 'dict[T3, list[T4]]', **kwargs):
            ret = {**kwargs}

            for dict in list(d2) + [d1]:
                for k, v in dict.items():
                    ret.setdefault(k, []).extend(v)

            return ret

        self.ids = concat(self.ids, elm.inner_html.ids, {elm.get_prop("id", None): [elm]})
        self.classes = concat(self.classes, elm.inner_html.classes, {c: [elm] for c in elm.classes})
        self.tags = concat(self.tags, elm.inner_html.tags, {type(elm): [elm]})

    def get_elements_by_id(self, id: 'str'):
        return self.ids.get(id, [])

    def get_elements_by_class_name(self, class_name: 'str'):
        return self.classes.get(class_name, [])

    def get_elements_by_tag_name(self, tag: 'str'):
        return self.tags.get(tag, [])

    @property
    def id(self):
        return Fetcher(self.children_ids, [])

    @property
    def cls(self):
        return Fetcher(self.children_classes, [])

    @property
    def tag(self):
        return Fetcher(self.children_tags, [])