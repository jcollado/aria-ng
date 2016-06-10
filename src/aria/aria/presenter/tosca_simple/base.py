
class Base(object):
    def __init__(self, raw={}):
        self.raw = raw

    def _get_primitive(self, name, default=None):
        return self.raw.get(name, default)

    def _get_primitive_list(self, name):
        return self.raw.get(name) or []

    def _get_object(self, name, cls):
        raw = self.raw.get(name)
        return cls(raw) if raw else None

    def _get_object_list(self, name, cls):
        structures = self.raw.get(name)
        return [cls(raw) for raw in structures] if structures else []

    def _get_object_dict(self, name, cls):
        structures = self.raw.get(name)
        return {name: cls(raw) for name, raw in structures.iteritems()} if structures else {}
