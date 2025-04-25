import json


def convert_template_v2_to_v3(template, template_id):

    type_mapping = {1: 1, 2: 2, 3: 3, 4: 2}  # adjust as needed
    mapped_type = type_mapping.get(template["type"])

    if mapped_type is None:
        print(f"Skipping unsupported type {template['type']} for template {
              template.get('title', '<no title>')}")
        return None

    # ...
    new_template = {
        "id": template_id,
        "type": mapped_type,
        "title": template["title"],
        "description": template.get("description", ""),
        "categories": template.get("categories", []),
        "platform": template.get("platform", ""),
        "logo": template.get("logo", ""),
        "image": template.get("image", "")
    }

    if "ports" in template:
        new_template["ports"] = template["ports"]

    if "volumes" in template:
        new_template["volumes"] = [
            {
                "container": vol["container"],
                **({"bind": vol["bind"]} if "bind" in vol else {})
            } for vol in template["volumes"]
        ]

    if "environment" in template:
        new_template["env"] = [
            {
                "name": e["name"],
                **({"label": e["label"]} if "label" in e else {})
            } for e in template["environment"]
        ]

    # Optional fields
    for field in ["command", "interactive", "note"]:
        if field in template:
            new_template[field] = template[field]

    return new_template


def convert_file(input_path, output_path):
    with open(input_path, "r") as f:
        v2_data = json.load(f)

    v3_data = {
        "version": "3",
        "templates": []
    }

    for idx, template in enumerate(v2_data.get("templates", []), start=1):
        v3_template = convert_template_v2_to_v3(template, idx)
        v3_data["templates"].append(v3_template)

    with open(output_path, "w") as f:
        json.dump(v3_data, f, indent=2)

    print(f"Conversion complete. Output written to {output_path}")


# Example usage:
convert_file("templates.json", "templates_v3.json")
