def validate_model(model_data):

    # --------------------------------------------------
    # BASIC VALIDATION
    # --------------------------------------------------
    if not isinstance(model_data, dict) or not model_data:
        raise ValueError("Parsed model is empty or invalid")

    # --------------------------------------------------
    # SUPPORT BOTH FORMATS
    # --------------------------------------------------
    if "classes" in model_data:
        classes = model_data.get("classes")
        associations = model_data.get("associations", [])
    else:
        # backward compatibility
        classes = model_data
        associations = []

    if not isinstance(classes, dict) or not classes:
        raise ValueError("Parsed class model is empty or invalid")

    if not isinstance(associations, list):
        raise ValueError("Associations must be a list")

    # --------------------------------------------------
    # CLASS + ATTRIBUTE VALIDATION
    # --------------------------------------------------
    class_names = set()

    for class_name, attributes in classes.items():

        if not isinstance(class_name, str) or not class_name.strip():
            raise ValueError("Class with empty name found")

        if class_name in class_names:
            raise ValueError(f"Duplicate class name: {class_name}")

        class_names.add(class_name)

        if not isinstance(attributes, list):
            raise ValueError(
                f"Invalid attribute structure in class '{class_name}'"
            )

        attr_names = set()

        for attr in attributes:

            if not isinstance(attr, dict):
                raise ValueError(
                    f"Malformed attribute in class '{class_name}'"
                )

            if "name" not in attr or "type" not in attr:
                raise ValueError(
                    f"Malformed attribute in class '{class_name}'"
                )

            if not attr["name"].strip():
                raise ValueError(
                    f"Empty attribute name in class '{class_name}'"
                )

            if attr["name"] in attr_names:
                raise ValueError(
                    f"Duplicate attribute '{attr['name']}' in class '{class_name}'"
                )

            attr_names.add(attr["name"])

            if not attr["type"].strip():
                raise ValueError(
                    f"Empty attribute type in class '{class_name}'"
                )

            if attr["type"] == "unknown":
                raise ValueError(
                    f"Unresolved datatype in class '{class_name}', "
                    f"attribute '{attr['name']}'"
                )

    # --------------------------------------------------
    # ASSOCIATION VALIDATION (SPIRAL 3 CORE)
    # --------------------------------------------------
    valid_types = {"one-to-one", "one-to-many", "many-to-one", "many-to-many"}
    seen_associations = set()

    for association in associations:

        if not isinstance(association, dict):
            raise ValueError("Malformed association in model")

        source = association.get("source")
        target = association.get("target")
        rel_type = association.get("type")

        # Basic presence
        if not source or not target:
            raise ValueError("Association missing source or target")

        # Class existence
        if source not in class_names:
            raise ValueError(f"Association source class not found: {source}")

        if target not in class_names:
            raise ValueError(f"Association target class not found: {target}")

        # Type validation
        if rel_type not in valid_types:
            raise ValueError(f"Invalid association type: {rel_type}")

        # Duplicate detection
        key = (source, target, rel_type)
        if key in seen_associations:
            raise ValueError(
                f"Duplicate association: {source} → {target} ({rel_type})"
            )
        seen_associations.add(key)

        # Self-relation validation
        if source == target:
            if rel_type not in {"one-to-many", "many-to-one"}:
                raise ValueError(
                    f"Invalid self-relationship type: {rel_type}"
                )

        # FK naming conflict check (for non many-to-many)
        if rel_type != "many-to-many":
            fk_name = f"{target.lower()}_id"
            attrs = classes[source]

            existing_names = {a["name"] for a in attrs}
            if fk_name in existing_names:
                raise ValueError(
                    f"FK name conflict in class '{source}': '{fk_name}' already exists"
                )

        # Mark many-to-many for generator
        if rel_type == "many-to-many":
            association["junction_required"] = True

    # --------------------------------------------------
    # NORMALIZE OUTPUT STRUCTURE
    # --------------------------------------------------
    return {
        "classes": classes,
        "associations": associations
    }