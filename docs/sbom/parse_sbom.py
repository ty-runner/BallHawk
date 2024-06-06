import json

# Path to the SBOM JSON file
file_path = 'sbom.json'

# Set to store unique licenses
licenses = set()

try:
    with open(file_path, 'r') as file:
        data = json.load(file)
        
    if 'components' in data:
        for component in data['components']:
            if 'licenses' in component:
                for license_entry in component['licenses']:
                    license_info = license_entry.get('license', {})
                    # Extracting the ID, which should be the authoritative identifier
                    license_id = license_info.get('id')
                    # Only add license ID if it is present and not a generic description
                    if license_id and not license_id.startswith('declared license of'):
                        licenses.add(license_id)
                    else:
                        # If ID isn't appropriate, check for a name but filter out generic descriptions
                        license_name = license_info.get('name')
                        if license_name and not license_name.startswith('declared license of'):
                            licenses.add(license_name)

    # Print all unique licenses found
    if licenses:
        print("Licenses found:", ", ".join(licenses))
    else:
        print("No licenses found.")
except FileNotFoundError:
    print(f"Error: The file {file_path} does not exist.")
except json.JSONDecodeError:
    print("Error: The file is not a valid JSON document.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
