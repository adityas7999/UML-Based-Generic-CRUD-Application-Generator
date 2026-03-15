def validate_model(model_data):

    if not isinstance(model_data, dict) or not model_data:
        raise ValueError("Parsed model is empty or invalid")

    classes = model_data
    associations = []

    # Backward compatible: support both legacy {Class: [...]} and
    # new {"classes": {...}, "associations": [...]} structures.
    if "classes" in model_data:
        classes = model_data.get("classes")
        associations = model_data.get("associations", [])

        if not isinstance(classes, dict) or not classes:
            raise ValueError("Parsed class model is empty or invalid")
        if not isinstance(associations, list):
            raise ValueError("Associations must be a list")

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

    if "classes" in model_data:
        for association in associations:
            if not isinstance(association, dict):
                raise ValueError("Malformed association in model")

            source = association.get("source")
            target = association.get("target")
            rel_type = association.get("type")

            if source not in class_names:
                raise ValueError(f"Association source class not found: {source}")
            if target not in class_names:
                raise ValueError(f"Association target class not found: {target}")

            if not isinstance(rel_type, str) or not rel_type.strip():
                raise ValueError("Association type is missing or invalid")

    return model_data