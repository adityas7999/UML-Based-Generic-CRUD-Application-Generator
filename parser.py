import xml.etree.ElementTree as ET
import json
import os


def parse_xmi(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {
        "xmi": "http://schema.omg.org/spec/XMI/2.1",
        "uml": "http://schema.omg.org/spec/UML/2.0"
    }

    model_data = {}
    datatype_map = {}

    # -------------------------------
    # STEP 1: Extract DataTypes
    # -------------------------------
    for dt in root.findall(".//packagedElement[@xmi:type='uml:DataType']", ns):
        dt_id = dt.get("{http://schema.omg.org/spec/XMI/2.1}id")
        dt_name = dt.get("name")
        if dt_id and dt_name:
            datatype_map[dt_id] = dt_name

    # -------------------------------
    # STEP 2: Extract Classes
    # -------------------------------
    for cls in root.findall(".//packagedElement[@xmi:type='uml:Class']", ns):
        class_name = cls.get("name")
        if not class_name:
            continue

        attributes = []

        # -------------------------------
        # STEP 3: Extract Attributes
        # -------------------------------
        attribute_elements = []
        attribute_elements.extend(cls.findall(".//ownedAttribute"))
        attribute_elements.extend(cls.findall(".//uml:ownedAttribute", ns))

        for attr in attribute_elements:
            attr_name = attr.get("name")
            attr_type = attr.get("type")

            # Handle case where attribute name is ":" - use the datatype name instead
            if attr_name and attr_name.strip() == ":" and attr_type and attr_type in datatype_map:
                attr_name = datatype_map[attr_type]
            
            # Skip if attribute name is still empty or just ":"
            if not attr_name or attr_name.strip() == ":":
                continue

            resolved_type = None

            if attr_type and attr_type in datatype_map:
                resolved_type = datatype_map[attr_type]
            elif attr_type:
                resolved_type = attr_type
            else:
                type_element = attr.find(".//type")
                if type_element is not None:
                    href = type_element.get("href")
                    if href and "#" in href:
                        resolved_type = href.split("#")[-1]

            if not resolved_type:
                resolved_type = "Unknown"

            resolved_type = resolved_type.capitalize()

            attributes.append({
                "name": attr_name,
                "type": resolved_type
            })

        model_data[class_name] = attributes

    return model_data


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    xmi_file = os.path.join(script_dir, "Test models/model_complex.xmi")

    result = parse_xmi(xmi_file)
    print(json.dumps(result, indent=4))