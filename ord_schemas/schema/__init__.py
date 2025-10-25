import json
import importlib.resources as pkg_resources

PACKAGE_NAME = __package__  # your package name

def list_domains():
    """Return top-level schema domains (subfolders in schema/)."""
    package_dir = pkg_resources.files(PACKAGE_NAME)
    return [p.name for p in package_dir.iterdir() if p.is_dir()]

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
            # Make path relative to the domain folder
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
