from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader, TemplateNotFound


TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"
DEFAULT_OUTPUT_FILE = Path("generated_app") / "models.py"


def _sorted_classes(model_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    classes = model_data.get("classes", {}) if isinstance(model_data, dict) else {}
    if not isinstance(classes, dict):
        return []

    ordered_classes = []
    for class_name in sorted(classes.keys()):
        attributes = classes.get(class_name, [])
        if not isinstance(attributes, list):
            attributes = []

        # 1. Identify the Primary Key dynamically (Same logic as Repo/API)
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

        # 2. Collect the rest of the attributes
        other_attrs = []
        for attribute in attributes:
            if not isinstance(attribute, dict):
                continue
            
            name = attribute.get("name", "").strip()
            # Skip if it's the PK we just found, or a literal 'id'
            if name and name != pk_name and name.lower() != "id":
                other_attrs.append({
                    "name": name,
                    "type": attribute.get("type", "").strip(),
                })

        if class_name.strip():
            ordered_classes.append({
                "name": class_name.strip(),
                "pk_name": pk_name,
                "other_attributes": other_attrs
            })

    return ordered_classes


def generate_models(model_data: Dict[str, Any], output_file: str | Path = DEFAULT_OUTPUT_FILE) -> str:
    """Render UML classes into a simple Python models module."""

    classes = _sorted_classes(model_data)
    if not classes:
        raise ValueError("No classes available to generate models")

    try:
        environment = Environment(
            loader=FileSystemLoader(str(TEMPLATE_DIR)),
            keep_trailing_newline=True,
            trim_blocks=True,     # Keeps Jinja spacing clean
            lstrip_blocks=True    # Keeps Jinja spacing clean
        )
        template = environment.get_template("model_template.j2")
    except TemplateNotFound as exc:
        raise FileNotFoundError("model_template.j2 not found in code_generator/templates") from exc

    rendered_output = template.render(classes=classes).lstrip("\n").rstrip() + "\n"

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered_output, encoding="utf-8")

    print(f"Model file successfully generated and saved to {output_path}")
    return str(output_path)