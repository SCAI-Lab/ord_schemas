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



def list_schemas(domain=None, subfolder=None, with_path = False):
    """
    List all JSON schema files, recursively, optionally filtered by domain and/or subfolder.
    If with_path=True, returns the full path relative to the package root.
    Otherwise, returns paths relative to the domain folder, OR relative to the subfolder 
    if both domain and subfolder are provided.
    """
    schemas = []
    package_dir = pkg_resources.files(PACKAGE_NAME)
    
    if subfolder is not None and domain is None:
        raise ValueError("Cannot filter by 'subfolder' without specifying a 'domain'.")

    start_index = 0
    if domain is not None:
        start_index = 1
    if subfolder is not None:
        start_index = 2

    for path in package_dir.rglob("*.json"):
        relative_path = path.relative_to(package_dir)

        if domain is not None and relative_path.parts[0] != domain:
            continue
            
        if subfolder is not None:
            if len(relative_path.parts) < 2 or relative_path.parts[1] != subfolder:
                continue

        if with_path:
            schemas.append(relative_path.as_posix())
        else:
            relative_path_parts = relative_path.parts[start_index:]
            relative_schema_path = "/".join(relative_path_parts)
            schemas.append(relative_schema_path)
        
    return schemas


def load_schema(folder, schema_name):
    """
    Load a JSON schema by domain and relative path (supports nested folders).
    Example: load_schema("ros4hc/metadata", "meta1.json")
    """
    schema_file = f"{folder}/{schema_name}"
    package_dir = pkg_resources.files(PACKAGE_NAME)
    with package_dir.joinpath(schema_file).open("r") as f:
        return json.load(f)
    

def load_schema_from_path(schema_path):
    """
    Load a JSON schema by its full path relative to the package root.
    Example: load_schema_from_path("ros4hc/metadata/meta1.json")
    """
    package_dir = pkg_resources.files(PACKAGE_NAME)
    
    try:
        schema_file = package_dir.joinpath(schema_path)
        with schema_file.open("r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Schema not found at path: {schema_path} relative to package {PACKAGE_NAME}")
    

def load_schema(folder, schema_name):
    """
    Load a JSON schema by specifying the folder path and the schema file name.
    Example: load_schema("ros4hc/metadata", "meta1.json")
    
    This function acts as a wrapper for load_schema_from_path.
    """
    schema_path = f"{folder}/{schema_name}"
    return load_schema_from_path(schema_path)