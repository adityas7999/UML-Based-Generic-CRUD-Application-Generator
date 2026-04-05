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

        ordered_attributes = [
            {
                "name": attribute.get("name", "").strip(),
                "type": attribute.get("type", "").strip(),
            }
            for attribute in attributes
            if isinstance(attribute, dict)
            and attribute.get("name", "").strip()
            and attribute.get("name", "").strip().lower() != "id"
        ]

        ordered_classes.append({"name": class_name.strip(), "attributes": ordered_attributes})

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
