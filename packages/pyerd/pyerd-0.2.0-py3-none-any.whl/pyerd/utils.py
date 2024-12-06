
import inspect

from pyerd.constants import MODULE_EXCLUDES, PARENT_EXCLUDES
from pyerd.model_node import ModelNode


def get_classes(module):
    """Get classes in the given module

    Args:
        module: Python Module

    Returns:
        list: List of classes in module
    """
    classes = []
    for name, obj in inspect.getmembers(module):
        if name not in MODULE_EXCLUDES and inspect.isclass(obj):
            classes.append(obj)
    return classes


def get_nodes_for_classes(classes) -> list[ModelNode]:
    """Get ModelNodes for Python classes

    Args:
        classes: Python classes

    Returns:
        list[ModelNode]: List of ModelNodes
    """
    nodes = []

    for cls in classes:
        members = inspect.getmembers(cls)
        fields = {}
        for member in members:
            if member[0] == '__annotations__':
                fields = member[1]
        parents = [parent for parent in cls.__bases__ if parent.__name__ not in PARENT_EXCLUDES]
        nodes.append(ModelNode(name=cls.__name__, parents=parents, fields=fields))
    return nodes


def get_union_field_type(union_args: tuple) -> str:
    """For union args (Union.__args__) get the string representation 
    of the types of the union

    Args:
        union_args (tuple): Union.__args__

    Returns:
        str: Union args delimited by "|" 
    """
    union_types = [t.__name__ for t in union_args if t.__name__ not in ['NoneType']]
    field_type = " | ".join(union_types)
    return field_type