from dataclasses import dataclass


@dataclass
class ModelNode:
    name: str
    fields: dict[str, type]
    parents: list[str]