import datetime
import enum
from errors import SimpleError


def has_text(text):
    if text is None:
        return False
    return len(text.strip()) > 0


def add_formatter(excluded_fields=None, parents_to_add=None, children_to_add=None):
    if not excluded_fields:
        excluded_fields = []
    if not parents_to_add:
        parents_to_add = []
    if not children_to_add:
        children_to_add = []

    def create_func(target):
        def format(self):
            ret = {
                key: getattr(self, key) for key in self.__table__.columns.keys()
                if key not in excluded_fields
            }
            ret = {
                key: ret[key] if not isinstance(ret[key], enum.Enum) else ret[key].name for key in ret
            }
            parents = {key: str(getattr(self, key) if getattr(self, key) else '') for key in parents_to_add}
            children = {key: [o.format() for o in getattr(self, key)] for key in children_to_add}
            return {**ret, **parents, **children}

        setattr(target, 'format', format)
        return target

    return create_func
