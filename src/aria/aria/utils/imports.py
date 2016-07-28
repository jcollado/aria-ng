
def import_fullname(name, paths=[]):
    """
    Imports a variable or class based on a full name, optionally searching for it in the paths.
    """
    
    if name is None:
        return None
    
    def do_import(name):
        if name and ('.' in name):
            module_name, name = name.rsplit('.', 1)
            return getattr(__import__(module_name, fromlist=[name], level=0), name)
        else:
            raise ImportError('import not found: %s' % name)
    
    try:
        return do_import(name)
    except:
        for p in paths:
            try:
                return do_import('%s.%s' % (p, name))
            except Exception as e:
                raise ImportError('cannot import %s, because %s' % (name, e))

    raise ImportError('import not found: %s' % name)

def import_modules(name):
    """
    Imports a module and all its sub-modules, recursively. Relies on modules defining a 'MODULES' attribute
    listing their sub-module names.
    """
    
    module = __import__(name, fromlist=['MODULES'], level=0)
    if hasattr(module, 'MODULES'):
        for m in module.MODULES:
            import_modules('%s.%s' % (name, m))
