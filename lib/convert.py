import json


def convert_template_v2_to_v3(template, template_id):
    """
    Convert a single Portainer template from v2 to v3 schema.
    """
    new_template = {}

    # Assign required fields with direct mappings
    new_template['id'] = template_id
    new_template['type'] = template.get('type', 1)
    new_template['title'] = template.get('title', '')
    new_template['description'] = template.get('description', '')
    new_template['categories'] = template.get('categories', [])
    new_template['platform'] = template.get('platform', '')
    new_template['logo'] = template.get('logo', '')
    new_template['image'] = template.get('image', '')

    # Optional fields
    if 'ports' in template:
        new_template['ports'] = template['ports']

    if 'volumes' in template:
        # In v3, 'bind' is optional
        new_template['volumes'] = [
            {
                'container': vol['container'],
                **({'bind': vol['bind']} if 'bind' in vol else {})
            }
            for vol in template['volumes']
        ]

    if 'environment' in template:
        # Rename 'environment' to 'env'
        new_template['env'] = template['environment']

    if 'command' in template:
        new_template['command'] = template['command']

    if 'interactive' in template:
        new_template['interactive'] = template['interactive']

    if 'note' in template:
        new_template['note'] = template['note']

    return new_template


def convert_templates_file(input_file_path, output_file_path):
    """
    Convert a Portainer templates file from v2 to v3 schema.
    """
    with open(input_file_path, 'r') as infile:
        v2_data = json.load(infile)

    v3_data = {
        'version': '3',
        'templates': []
    }

    for idx, template in enumerate(v2_data.get('templates', []), start=1):
        v3_template = convert_template_v2_to_v3(template, idx)
        v3_data['templates'].append(v3_template)

    with open(output_file_path, 'w') as outfile:
        json.dump(v3_data, outfile, indent=2)

    print(f"Conversion complete. Output written to {output_file_path}")


# Example usage:
# convert_templates_file('templates_v2.json', 'templates_v3.json')
convert_templates_file('templates.json', 'templates_v3.json')
