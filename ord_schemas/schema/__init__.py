import json
import importlib.resources as pkg_resources

PACKAGE_NAME = __package__ 

def list_domains():
    """Return top-level schema domains (subfolders in schema/)."""
    with pkg_resources.files(PACKAGE_NAME) as package_dir:
        return [p.name for p in package_dir.iterdir() if p.is_dir()]

def list_schemas(domain=None):
    """List JSON schema files, optionally filtered by domain."""
    schemas = []
    with pkg_resources.files(PACKAGE_NAME) as package_dir:
        for path in package_dir.rglob("*.json"):
            relative_path = path.relative_to(package_dir)
            if domain is None or relative_path.parts[0] == domain:
                schemas.append(str(relative_path))
    return schemas

def load_schema(domain, schema_name):
    """Load a JSON schema by domain and name."""
    schema_file = f"{domain}/{schema_name}.json"
    with pkg_resources.files(PACKAGE_NAME).joinpath(schema_file).open("r") as f:
        return json.load(f)
