"""
Repository Layer Generator for CRUD Operations
Generated repository.py contains database access functions:
- insert()
- get_all()
- get_by_id()
- update()
- delete()

Uses parameterized queries for SQL injection safety.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

from jinja2 import Environment, FileSystemLoader, TemplateNotFound


TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"
DEFAULT_OUTPUT_FILE = Path("generated_app") / "repository.py"


def _sorted_classes_with_attributes(model_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract and sort classes with their attributes for deterministic output.
    Excludes 'id' attribute as it's auto-generated.
    """
    classes = model_data.get("classes", {}) if isinstance(model_data, dict) else {}
    if not isinstance(classes, dict):
        return []

    ordered_classes = []
    for class_name in sorted(classes.keys()):
        attributes = classes.get(class_name, [])
        if not isinstance(attributes, list):
            attributes = []

        # Filter out 'id' attribute as it's auto-generated
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

        ordered_classes.append({
            "name": class_name.strip(),
            "table_name": class_name.lower(),
            "attributes": ordered_attributes,
        })

    return ordered_classes


def generate_repository(
    model_data: Dict[str, Any],
    output_file: str | Path = DEFAULT_OUTPUT_FILE
) -> str:
    """
    Generate repository.py with CRUD functions for all classes.
    
    Functions generated per class:
    - insert_<classname>()
    - get_all_<classname>()
    - get_<classname>_by_id()
    - update_<classname>()
    - delete_<classname>()
    
    Uses parameterized queries for SQL injection safety.
    Includes basic error handling.
    """

    classes = _sorted_classes_with_attributes(model_data)
    if not classes:
        raise ValueError("No classes available to generate repository")

    try:
        environment = Environment(
            loader=FileSystemLoader(str(TEMPLATE_DIR)),
            keep_trailing_newline=True,
        )
        template = environment.get_template("repository_template.j2")
    except TemplateNotFound as exc:
        raise FileNotFoundError(
            "repository_template.j2 not found in code_generator/templates"
        ) from exc

    rendered_output = template.render(classes=classes).lstrip("\n").rstrip() + "\n"

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered_output, encoding="utf-8")

    print(f"Repository file successfully generated and saved to {output_path}")
    return str(output_path)
