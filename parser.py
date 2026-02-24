import xml.etree.ElementTree as ET
import json
import os


def parse_xmi(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError:
        raise ValueError("Malformed XML / Invalid XMI file")

    model_data = {}
    datatype_map = {}

    # -------------------------------------------------
    # STEP 1: Extract Primitive + Data Types
    # -------------------------------------------------
    for element in root.iter():

        if not element.tag.endswith("packagedElement"):
            continue

        xmi_type = element.attrib.get("{http://schema.omg.org/spec/XMI/2.1}type")
        element_id = element.attrib.get("{http://schema.omg.org/spec/XMI/2.1}id")
        element_name = element.attrib.get("name")

        if xmi_type in ["uml:PrimitiveType", "uml:DataType"]:
            if element_id and element_name:
                datatype_map[element_id] = element_name.lower()

    # -------------------------------------------------
    # STEP 2: Extract Classes
    # -------------------------------------------------
    for cls in root.iter():

        if not cls.tag.endswith("packagedElement"):
            continue

        xmi_type = cls.attrib.get("{http://schema.omg.org/spec/XMI/2.1}type")

        if xmi_type != "uml:Class":
            continue

        class_name = cls.attrib.get("name")

        if not class_name or not class_name.strip():
            continue

        attributes = []

        # Direct ownedAttribute only
        for attr in cls:

            if not attr.tag.endswith("ownedAttribute"):
                continue

            attr_name = attr.attrib.get("name")

            if not attr_name or not attr_name.strip():
                continue

            resolved_type = None
            attr_type = attr.attrib.get("type")

            # Case 1: Referenced by ID
            if attr_type and attr_type in datatype_map:
                resolved_type = datatype_map[attr_type]

            # Case 2: Direct string type
            elif attr_type:
                resolved_type = attr_type.lower()

            # Case 3: Nested <type href=...>
            else:
                for child in attr:
                    if child.tag.endswith("type"):
                        href = child.attrib.get("href")
                        if href and "#" in href:
                            resolved_type = href.split("#")[-1].lower()

            if not resolved_type:
                resolved_type = "unknown"

            attributes.append({
                "name": attr_name.strip(),
                "type": resolved_type
            })

        model_data[class_name.strip()] = attributes

    if not model_data:
        raise ValueError("No UML Classes found in XMI")

    return model_data
