import xml.etree.ElementTree as ET
import json
import os


XMI_NS = "{http://schema.omg.org/spec/XMI/2.1}"


def _extract_multiplicity(association_end):
    lower = "1"
    upper = "1"

    for child in association_end:
        if child.tag.endswith("lowerValue"):
            lower = child.attrib.get("value", "1")
        elif child.tag.endswith("upperValue"):
            upper = child.attrib.get("value", "1")

    return lower, upper


def _is_many(upper):
    if upper == "*":
        return True
    if upper.isdigit() and int(upper) > 1:
        return True
    return False


def _association_type(source_multiplicity, target_multiplicity):
    _, source_upper = source_multiplicity
    _, target_upper = target_multiplicity

    source_many = _is_many(source_upper)
    target_many = _is_many(target_upper)

    if source_many and target_many:
        return "many-to-many"
    if source_many and not target_many:
        return "many-to-one"
    if not source_many and target_many:
        return "one-to-many"
    return "one-to-one"


def parse_xmi(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError:
        raise ValueError("Malformed XML / Invalid XMI file")

    class_data = {}
    associations = []
    datatype_map = {}
    class_id_map = {}

    # -------------------------------------------------
    # STEP 1: Extract Primitive + Data Types
    # -------------------------------------------------
    for element in root.iter():

        if not element.tag.endswith("packagedElement"):
            continue

        xmi_type = element.attrib.get(f"{XMI_NS}type")
        element_id = element.attrib.get(f"{XMI_NS}id")
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

        xmi_type = cls.attrib.get(f"{XMI_NS}type")

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

        class_name = class_name.strip()
        class_data[class_name] = attributes

        class_id = cls.attrib.get(f"{XMI_NS}id")
        if class_id:
            class_id_map[class_id] = class_name

    # -------------------------------------------------
    # STEP 3: Extract Associations
    # -------------------------------------------------
    for element in root.iter():

        xmi_type = element.attrib.get(f"{XMI_NS}type")
        if xmi_type != "uml:Association":
            continue

        association_ends = []
        for child in element:
            child_type = child.attrib.get(f"{XMI_NS}type")
            if child.tag.endswith("ownedEnd") or child_type == "uml:Property":
                end_type_id = child.attrib.get("type")
                class_name = class_id_map.get(end_type_id)
                if not class_name:
                    continue

                lower, upper = _extract_multiplicity(child)
                association_ends.append({
                    "class": class_name,
                    "multiplicity": {
                        "lower": lower,
                        "upper": upper
                    }
                })

        if len(association_ends) < 2:
            continue

        source = association_ends[0]
        target = association_ends[1]
        associations.append({
            "source": source["class"],
            "target": target["class"],
            "direction": "source-to-target",
            "multiplicity": {
                "source": source["multiplicity"],
                "target": target["multiplicity"]
            },
            "type": _association_type(
                (source["multiplicity"]["lower"], source["multiplicity"]["upper"]),
                (target["multiplicity"]["lower"], target["multiplicity"]["upper"])
            )
        })

    if not class_data:
        raise ValueError("No UML Classes found in XMI")

    return {
        "classes": class_data,
        "associations": associations
    }
