def validate_model(model_data):

    if not isinstance(model_data, dict) or not model_data:
        raise ValueError("Parsed model is empty or invalid")

    class_names = set()

    for class_name, attributes in model_data.items():

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

    return model_data