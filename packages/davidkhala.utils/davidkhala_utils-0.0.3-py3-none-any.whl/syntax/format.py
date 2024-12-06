import json
from abc import ABC, abstractmethod


def JSONReadable(data):
    return json.dumps(data, indent=4, sort_keys=True)

class Serializable(ABC):
    
    @abstractmethod
    def as_dict(self) -> dict:
        pass