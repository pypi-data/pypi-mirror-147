import ruamel.yaml, json
# from self.yaml.loader import FullLoader
# from self.yaml.loader import SafeLoader
# from self.yaml.loader import BaseLoader
# from self.yaml.loader import UnsafeLoader


class DarkYaml:
    def __init__(self, filepth, typ='rt'):
        self.filepth = filepth
        self.yaml = ruamel.yaml.YAML(typ=typ)
        self.yaml.indent(sequence=4, offset=2)
        
        self.get = self.__getitem__
        self.set = self.__setitem__
    
        
    def __getitem__(self, item):
        return self._load()[item]
    
    def __setitem__(self, key, item):
        data = self._load()
        data[key] = item
        
        self._dump(data)
        
    def _dump(self, data):
        with open(self.filepth, 'w') as file:
            self.yaml.dump(data, file)
    
    def _load(self):
        with open(self.filepth, 'r') as file:
            return self.yaml.load(file)
        
    
    def __str__(self):
        return json.dumps(self._load(), indent=8)
   
    def __repr__(self):
        return json.dumps(self._load(), indent=8)