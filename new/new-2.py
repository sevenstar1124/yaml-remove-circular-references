import yaml
from openapi_spec_validator import openapi_v3_spec_validator
from collections import deque

def find_circular_references(spec):
    ref_map = {}
    path_queue = deque([((), spec)])
    while path_queue:
        path, current = path_queue.popleft()
        if isinstance(current, dict):
            for key, value in current.items():
                if key == '$ref':
                    ref_path = tuple(value.split('/'))
                    full_path = path + (key,)
                    if ref_path in ref_map:
                        ref_map[ref_path].append(full_path)
                    else:
                        ref_map[ref_path] = [full_path]
                else:
                    path_queue.append((path + (key,), value))
        elif isinstance(current, list):
            for index, item in enumerate(current):
                path_queue.append((path + (index,), item))
    return {k: v for k, v in ref_map.items() if len(v) > 1}

def remove_circular_references(yaml_data):
    spec = yaml.load(yaml_data, Loader=yaml.SafeLoader)
    circular_references = find_circular_references(spec)
    
    for ref_path, occurences in circular_references.items():
        for occurrence in occurences[1:]:
            parent = spec
            for part in occurrence[:-1]:
                parent = parent[part]
            del parent[occurrence[-1]]
            
    return yaml.dump(spec, sort_keys=False)

# Load the OpenAPI YAML file 
with open('1.yaml', 'r') as file:
    yaml_data = file.read()

cleaned_yaml = remove_circular_references(yaml_data)

# Save the cleaned OpenAPI YAML file
with open('cleaned_openapi-2.yaml', 'w') as file:
    file.write(cleaned_yaml)
