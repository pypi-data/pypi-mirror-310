class SymbolTable(dict):
    def __init__(self, parent=None):
        self.parent = parent

    def __setitem__(self, key, value):
        try:
            self[key]
            if key in self:
                dict.__setitem__(self, key, value)
            else:
                self.parent[key] = value
        except KeyError:
            dict.__setitem__(self, key, value)

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            if self.parent is not None:
                return self.parent[key]
            else:
                raise KeyError

    def get(self, key):
        return self[key]

    def set(self, key, value):
        self[key] = value

    def has_key(self, key):
        return key in self

    def push(self):
        return SymbolTable(self)

    def pop(self):
        return self.parent
