"""
Repository Layer Generator for CRUD Operations
Uses dynamic Primary Keys detected from UML models.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"
DEFAULT_OUTPUT_FILE = Path("generated_app") / "repository.py"

def _sorted_classes_with_attributes(model_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    classes = model_data.get("classes", {}) if isinstance(model_data, dict) else {}
    if not isinstance(classes, dict): return []

    ordered_classes = []
    for class_name in sorted(classes.keys()):
        attributes = classes.get(class_name, [])
        if not isinstance(attributes, list): attributes = []

        # 1. Identify the Primary Key dynamically
        pk_name = "id"
        found_pk = False
        
        for attr in attributes:
            name = attr.get("name", "").strip()
            # Standard PK naming conventions
            if name.lower() in ["id", f"{class_name.lower()}id"]:
                pk_name = name
                found_pk = True
                break
                
        # Fallback: Assume first attribute is the PK
        if not found_pk and attributes:
            pk_name = attributes[0].get("name", "id").strip()

        # 2. Filter attributes for precise queries
        all_attrs = []
        insert_attrs = []
        update_attrs = []

        for attr in attributes:
            if not isinstance(attr, dict): continue
            name = attr.get("name", "").strip()
            typ = attr.get("type", "string").strip()
            if not name: continue
            
            all_attrs.append({"name": name, "type": typ})
            
            # Exclude literal 'id' from insert (assuming DB auto-increments it)
            if name.lower() != "id":
                insert_attrs.append({"name": name, "type": typ})
            
            # Exclude literal 'id' AND the dynamic Primary Key from UPDATE SET clause
            if name.lower() != "id" and name != pk_name:
                update_attrs.append({"name": name, "type": typ})

        if class_name.strip():
            ordered_classes.append({
                "name": class_name.strip(),
                "table_name": class_name.strip(), # Match exact case of SQL table
                "pk_name": pk_name,
                "all_attributes": all_attrs,
                "insert_attributes": insert_attrs,
                "update_attributes": update_attrs,
            })

    return ordered_classes

def generate_repository(model_data: Dict[str, Any], output_file: str | Path = DEFAULT_OUTPUT_FILE) -> str:
    classes = _sorted_classes_with_attributes(model_data)
    if not classes:
        raise ValueError("No classes available to generate repository")

    try:
        environment = Environment(
            loader=FileSystemLoader(str(TEMPLATE_DIR)),
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
        template = environment.get_template("repository_template.j2")
    except TemplateNotFound as exc:
        raise FileNotFoundError("repository_template.j2 not found") from exc

    rendered_output = template.render(classes=classes).lstrip("\n").rstrip() + "\n"
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered_output, encoding="utf-8")
    print(f"Repository file successfully generated and saved to {output_path}")
    return str(output_path)