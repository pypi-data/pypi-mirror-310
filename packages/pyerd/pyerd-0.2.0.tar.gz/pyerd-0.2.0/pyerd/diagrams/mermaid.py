
from pyerd.model_node import ModelNode
from pyerd.utils import get_union_field_type


def nodes_to_mermaid(nodes: list[ModelNode]) -> str:
    title = """---
title: From models
---"""
    classes = []
    links = []
    
    node_names = [node.name for node in nodes]
    
    for node in nodes:
        # Need to convert field values to strings
        # Go through fields and identify not primitives
        fields = []
        for field in node.fields.keys():
            node_field: type | None = node.fields.get(field)
            
            if node_field is None:
                continue

            if hasattr(node_field, "__name__") and node_field.__name__ == "Union":
                field_type = get_union_field_type(node_field.__args__)
            elif type(node_field).__name__ == "UnionType":
                field_type = get_union_field_type(node_field.__args__)
            else:
                field_type = str(node_field.__name__) # pyright: ignore reportOptionalMemberAccess
            field = f"{field_type} {field}"
            fields.append(field)
            if field_type in node_names:
                # Create link
                links.append(f"{node.name} *-- {field_type}")

        field_str = "\n".join(fields)
        class_str = f"""
class {node.name}{"{"}
    {field_str}
{"}"}"""
        classes.append(class_str)
        
        if node.parents:
            # Then parent <|-- child
            link_strs = [f"{parent.__name__} <|-- {node.name}" for parent in node.parents] # pyright: ignore reportAttributeAccessIssue
            links.extend(link_strs)
            
    # Put them all together
    link_str = "\n".join(links)
    class_str = "\n".join(classes)
    mermaid_diagram = f"""
{title}
classDiagram
{link_str}
    {class_str}
    """
    return mermaid_diagram