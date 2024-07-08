import yaml
from openapi_spec_validator import validate_spec
import sys

def load_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def save_yaml(data, file_path):
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

def flatten_refs(spec):
    # Simplify complex objects to basic IDs to avoid circular refs
    schemas = spec.get('components', {}).get('schemas', {})
    for name, schema in schemas.items():
        if 'properties' in schema:
            for prop_name, prop in schema['properties'].items():
                if '$ref' in prop:
                    ref_name = prop['$ref'].split('/')[-1]
                    if ref_name in schemas:
                        print(f'{prop_name}, {prop}, {ref_name}')
                        print("\n")

                        schema['properties'][prop_name] = {
                            "type": "integer",  # assuming ID is integer type
                            "description": f"Reference to {ref_name} ID"
                        }
    return spec

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python resolve_circular_refs.py <path_to_openapi_yaml>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    spec = load_yaml(file_path)

    # Validate before modification
    try:
        validate_spec(spec)
        print("Original spec is valid.")
    except Exception as e:
        print("Validation error in original spec:", e)

    # Flatten references
    cleaned_spec = flatten_refs(spec)

    # Validate after modification
    try:
        validate_spec(cleaned_spec)
        print("Cleaned spec is valid.")
    except Exception as e:
        print("Validation error in cleaned spec:", e)

    # Save the modified spec
    output_file_path = "cleaned_" + file_path
    save_yaml(cleaned_spec, output_file_path)
    print(f"Cleaned spec saved to {output_file_path}")
