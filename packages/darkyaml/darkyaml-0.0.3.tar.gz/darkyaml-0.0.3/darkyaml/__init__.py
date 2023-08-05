import ruamel.yaml, json

class DarkYaml(dict):
    def __init__(self, filepth, typ='rt'):
        super().__init__()
        
        self.filepth = filepth
        self.yaml = ruamel.yaml.YAML(typ=typ)
        self.yaml.indent(sequence=4, offset=2)
        
        self.update(self._load())
    
    def _dump(self, data):
        
        
        with open(self.filepth, 'w') as file:
            self.yaml.dump(dict(data), file)
    
    def _load(self):
        with open(self.filepth, 'r') as file:
            return self.yaml.load(file)
            
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._dump(self)
        
    def __delitem__(self, key):
        super().__delitem__(key)
        self._dump(self)
        
    
    def pop(self, key):
        super().pop(key)
        self._dump(self)
        
    def popitem(self):
        super().popitem()
        self._dump(self)
        
    def update(self, dc):
        super().update(dc)
        self._dump(self)
        
    def clear(self):
        super().clear()
        self._dump(self)
        