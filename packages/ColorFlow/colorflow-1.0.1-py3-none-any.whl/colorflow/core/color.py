from dataclasses import dataclass
from typing import Tuple

@dataclass(slots=True, frozen=True)
class Color:
    r: int
    g: int
    b: int
    
    def __post_init__(self):
        object.__setattr__(self, 'r', max(0, min(255, self.r)))
        object.__setattr__(self, 'g', max(0, min(255, self.g)))
        object.__setattr__(self, 'b', max(0, min(255, self.b)))
    
    def __str__(self) -> str:
        return f"RGB({self.r}, {self.g}, {self.b})"
    
    def to_tuple(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)
    
    def to_hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    def __call__(self, text: str) -> str:
        return f"\033[38;2;{self.r};{self.g};{self.b}m{text}\033[0m"