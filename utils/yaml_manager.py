import yaml
from dataclasses import dataclass,field
from typing import Dict

@dataclass
class YamlManger:
    """"""
    file_path:str

    def read_as_json(self)->Dict:
        with open(self.file_path) as f:
            data = yaml.safe_load(f)
        return data

    def write_to_yaml(self,content,file_path)->None:
        with open(file_path,'w') as f:
            yaml.dump(content,f)