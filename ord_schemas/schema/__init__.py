import json
import importlib.resources as pkg_resources

PACKAGE_NAME = __package__ 

def list_domains():
    """Return top-level schema domains (subfolders in schema/)."""
    package_dir = pkg_resources.files(PACKAGE_NAME)
    return [p.name for p in package_dir.iterdir() if p.is_dir() and p.name != "__pycache"]


def _format_tree(path, prefix = ''):
    """
    Helper function to recursively format the directory structure as a string tree, 
    using only built-in string characters.
    """

    tree_lines = []

    items = sorted([
        item
        for item in path.iterdir()
        if item.is_dir() and item.name != "__pycache__"
    ], key = lambda p : p.name)

    count = len(items)
    for i, item in enumerate(items):
        is_last = (i == count -1)

        connector = "└── " if is_last else "├── "
        tree_lines.append(f"{prefix}{connector}{item.name}")

        childPrefix = prefix + (' ' * 4 if is_last else "|" + ' ' * 3)
        tree_lines.extend(_format_tree(item, childPrefix))

    return tree_lines


def get_tree_structure():
    """
    Loads the entire folder structure (domain subfolders and nested subfolders) 
    of the package as a nested dictionary, excluding files and __pycache__.
    """
    package_dir = pkg_resources.files(PACKAGE_NAME)

    tree_lines = _format_tree(package_dir)
    root_name = PACKAGE_NAME.split('.')[-1] if '.' in PACKAGE_NAME else PACKAGE_NAME

    return f"{root_name}/\n" + "\n".join(tree_lines)



def list_schemas(domain=None):
    """
    List all JSON schema files, recursively, optionally filtered by domain.
    Returns paths relative to the domain folder.
    """
    schemas = []
    package_dir = pkg_resources.files(PACKAGE_NAME)
    
    for path in package_dir.rglob("*.json"):
        relative_path = path.relative_to(package_dir)
        if domain is None or relative_path.parts[0] == domain:
            relative_to_domain = "/".join(relative_path.parts[1:])
            schemas.append(relative_to_domain)
    
    return schemas


def load_schema(domain, schema_relative_path):
    """
    Load a JSON schema by domain and relative path (supports nested folders).
    Example: load_schema("ros4hc", "metadata/meta1.json")
    """
    schema_file = f"{domain}/{schema_relative_path}"
    package_dir = pkg_resources.files(PACKAGE_NAME)
    with package_dir.joinpath(schema_file).open("r") as f:
        return json.load(f)
