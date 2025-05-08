from dataclasses import dataclass, asdict



@dataclass
class Terminology:
    def to_dict(self):
        return asdict(self)