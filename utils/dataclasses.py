from dataclasses import dataclass

@dataclass
class RoleCategory:
    name: str

    def __post_init__(self):
        self.name = f"\u2063{self.name:{'\u2002'}^{34}}{'\u2002' * 5}\u2063"
