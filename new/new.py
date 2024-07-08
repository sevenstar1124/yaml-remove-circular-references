import yaml

def break_circular_refs(data, path=None):
    if path is None:
        path = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = path + [key]
            if isinstance(value, (dict, list)):
                if new_path in path:
                    data[key] = f"Circular reference to {'.'.join(new_path)}"
                else:
                    data[key] = break_circular_refs(value, new_path)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = path + [str(i)]
            if isinstance(item, (dict, list)):
                if new_path in path:
                    data[i] = f"Circular reference to {'.'.join(new_path)}"
                else:
                    data[i] = break_circular_refs(item, new_path)
    
    return data

# Load your YAML
with open('1.yaml', 'r') as file:
    spec = yaml.safe_load(file)

# Break circular references
cleaned_spec = break_circular_refs(spec)

# Save the cleaned YAML
with open('cleaned_openapi.yaml', 'w') as file:
    yaml.dump(cleaned_spec, file)