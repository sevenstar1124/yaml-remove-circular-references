from openapi_spec_validator import validate_spec
from openapi_spec_validator.exceptions import OpenAPISpecValidatorError
import yaml

# Load the original OpenAPI schema
with open('1.yaml', 'r') as f:
    original_spec = yaml.safe_load(f)

# Validate the original spec and resolve circular references
try:
    validate_spec(original_spec)
    print("Original OpenAPI spec is valid!")
except OpenAPISpecValidatorError as e:
    # If there are circular references, resolve them
    resolved_spec = e.resolvent
    
    # Save the resolved spec to a new file
    with open('2.yaml', 'w') as f:
        yaml.dump(resolved_spec, f)
    print("Cleaned-up OpenAPI spec saved!")