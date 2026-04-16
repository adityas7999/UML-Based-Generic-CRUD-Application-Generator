from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader, TemplateNotFound


TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"
DEFAULT_OUTPUT_FILE = Path("generated_app") / "app.py"

def _sorted_classes(model_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    classes = model_data.get("classes", {}) if isinstance(model_data, dict) else {}
    if not isinstance(classes, dict): return []

    ordered_classes = []
    for class_name in sorted(classes.keys()):
        attributes = classes.get(class_name, [])
        if not isinstance(attributes, list): attributes = []

        pk_name = "id"
        found_pk = False
        for attr in attributes:
            name = attr.get("name", "").strip()
            if name.lower() in ["id", f"{class_name.lower()}id"]:
                pk_name = name
                found_pk = True
                break
                
        if not found_pk and attributes:
            pk_name = attributes[0].get("name", "id").strip()

        insert_attrs = []
        update_attrs = []

        for attr in attributes:
            if not isinstance(attr, dict): continue
            name = attr.get("name", "").strip()
            typ = attr.get("type", "string").strip()
            if not name: continue
            
            if name.lower() != "id":
                insert_attrs.append({"name": name, "type": typ})
            if name.lower() != "id" and name != pk_name:
                update_attrs.append({"name": name, "type": typ})

        if class_name.strip():
            ordered_classes.append({
                "name": class_name.strip(),
                "pk_name": pk_name,
                "insert_attributes": insert_attrs,
                "update_attributes": update_attrs,
            })
    return ordered_classes

def generate_api(
    model_data: Dict[str, Any],
    output_file: str | Path = DEFAULT_OUTPUT_FILE
) -> str:
    """
    Generate Flask API (app.py) from UML model.

    Output:
    - REST endpoints for each class using repository functions
    """

    classes = _sorted_classes(model_data)
    if not classes:
        raise ValueError("No classes available to generate API")

    try:
        env = Environment(
            loader=FileSystemLoader(str(TEMPLATE_DIR)),
            keep_trailing_newline=True,
            trim_blocks=True,     # Added to assist with whitespace cleanup
            lstrip_blocks=True    # Added to assist with whitespace cleanup
        )
        template = env.get_template("api_template.j2")
    except TemplateNotFound as exc:
        raise FileNotFoundError(
            "api_template.j2 not found in code_generator/templates"
        ) from exc

    rendered_output = template.render(classes=classes).lstrip("\n").rstrip() + "\n"

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered_output, encoding="utf-8")

    print(f"Flask API successfully generated and saved to {output_path}")
    return str(output_path)