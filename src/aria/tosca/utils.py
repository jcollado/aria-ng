
class Dynamic(object):
    def __init__(self, raw, definitions):
        self._structure = raw
        self._definitions= definitions

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError:
            for k, v in self._definitions.iteritems():
                if k == name:
                    return self._structure.get(k)
            raise AttributeError(name)

    def __setattr__(self, name, value):
        try:
            self.__dict__[name] = value
        except KeyError:
            for k, v in self._definitions.iteritems():
                if k == name:
                    self._structure[k] = value
                    return
            raise AttributeError(name)

class HasProperties(object):
    def __init__(self, raw={}):
        self.raw = raw

    @property
    def properties(self):
        properties = HasProperties._get_class_properties(self.__class__)
        return Dynamic(self.raw.get('properties', {}), properties)

    @staticmethod
    def _get_class_properties(cls):
        properties = {}
        for base_cls in cls.__bases__:
            properties.update(HasProperties._get_class_properties(base_cls))
        if hasattr(cls, 'PROPERTIES'):
            properties.update(cls.PROPERTIES)
        return properties

class HasConstraints(object):
    def __init__(self, raw={}):
        self.raw = raw

    @property
    def constraints(self):
        constraints = HasConstraints._get_class_constraints(self.__class__)
        return Dynamic(self.raw.get('constraints', {}), constraints)

    @staticmethod
    def _get_class_constraints(cls):
        constraints = {}
        for base_cls in cls.__bases__:
            constraints.update(HasConstraints._get_class_constraints(base_cls))
        if hasattr(cls, 'CONSTRAINTS'):
            constraints.update(cls.CONSTRAINTS)
        return constraints
