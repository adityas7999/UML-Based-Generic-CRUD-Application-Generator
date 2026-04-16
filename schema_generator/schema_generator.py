import os
from schema_generator.type_mapper import map_type

def generate_schema(model_data, output_file="schema.sql", db_name="uml_crud_db"):

    sql_statements = [
        f"CREATE DATABASE IF NOT EXISTS `{db_name}`;",
        f"USE `{db_name}`;\n"
    ]

    classes_dict = model_data.get("classes", {})
    associations = model_data.get("associations", [])

    sorted_class_names = sorted(classes_dict.keys())
    sorted_associations = sorted(associations, key=lambda x: (x.get("source", ""), x.get("target", "")))

    # ================================
    # STEP 0: PRECOMPUTE PRIMARY KEYS
    # ================================
    class_pks = {}
    for class_name in sorted_class_names:
        attributes = classes_dict.get(class_name, [])
        pk_name = "id"
        pk_type = "int"
        found_pk = False
        
        for attr in attributes:
            name = attr.get("name", "").strip()
            # Match API/Repo logic: Look for 'id' or '<classname>id'
            if name.lower() in ["id", f"{class_name.lower()}id"]:
                pk_name = name
                pk_type = attr.get("type", "int")
                found_pk = True
                break
                
        # Fallback to the first attribute
        if not found_pk and attributes:
            pk_name = attributes[0].get("name", "id").strip()
            pk_type = attributes[0].get("type", "int")
            
        class_pks[class_name] = {
            "name": pk_name, 
            "type": map_type(pk_type) # Map UML type to SQL type immediately
        }

    table_columns = {name: [] for name in sorted_class_names}
    fk_constraints = []
    junction_tables = []
    added_fk_columns = {name: set() for name in sorted_class_names}

    # ================================
    # STEP 1: PREPARE FK COLUMNS ONLY
    # ================================
    for assoc in sorted_associations:
        source = assoc.get("source")
        target = assoc.get("target")
        rel_type = assoc.get("type", "").lower()

        if not source or not target or source not in class_pks or target not in class_pks:
            continue

        is_self = source == target

        if rel_type == "many-to-many":
            sorted_pair = sorted([source, target])
            s1, s2 = sorted_pair[0], sorted_pair[1]
            
            pk1 = class_pks[s1]["name"]
            pk2 = class_pks[s2]["name"]
            type1 = class_pks[s1]["type"]
            type2 = class_pks[s2]["type"]

            j_table = f"{s1}_{s2}"

            # e.g., course_courseId
            col1 = f"{s1.lower()}_{pk1}_1" if is_self else f"{s1.lower()}_{pk1}"
            col2 = f"{s2.lower()}_{pk2}_2" if is_self else f"{s2.lower()}_{pk2}"

            junction_sql = f"""CREATE TABLE `{j_table}` (
    `{col1}` {type1},
    `{col2}` {type2}
);"""

            fk_constraints.append(f"ALTER TABLE `{j_table}` ADD FOREIGN KEY (`{col1}`) REFERENCES `{s1}`(`{pk1}`);")
            fk_constraints.append(f"ALTER TABLE `{j_table}` ADD FOREIGN KEY (`{col2}`) REFERENCES `{s2}`(`{pk2}`);")

            junction_tables.append(junction_sql)
            continue

        child, parent = None, None
        unique = False

        if rel_type == "one-to-many":
            child, parent = target, source
        elif rel_type == "many-to-one":
            child, parent = source, target
        elif rel_type in ["one-to-one", "1:1"]:
            child, parent = source, target
            unique = True

        if not child or not parent or child not in class_pks or parent not in class_pks:
            continue

        parent_pk = class_pks[parent]["name"]
        parent_type = class_pks[parent]["type"]

        # Creates a descriptive FK column (e.g. department_deptId)
        fk_col = f"{parent.lower()}_{parent_pk}"
        if is_self:
            fk_col = f"parent_{fk_col}"

        if fk_col in added_fk_columns[child]:
            continue

        added_fk_columns[child].add(fk_col)

        unique_str = " UNIQUE" if unique else ""
        table_columns[child].append(f"`{fk_col}` {parent_type}{unique_str}")

        fk_constraints.append(
            f"ALTER TABLE `{child}` ADD FOREIGN KEY (`{fk_col}`) REFERENCES `{parent}`(`{parent_pk}`);"
        )

    # ================================
    # STEP 2: CREATE TABLES (NO FKs)
    # ================================
    for class_name in sorted_class_names:
        attributes = classes_dict.get(class_name, [])
        pk_info = class_pks[class_name]
        pk_name = pk_info["name"]

        columns = []
        pk_added = False

        for attr in attributes:
            name = attr.get("name", "").strip()
            if not name:
                continue
                
            attr_type = map_type(attr.get("type"))
            
            if name == pk_name:
                # Only Auto-Increment if the field is literally "id" and an INT
                auto_inc = " AUTO_INCREMENT" if name.lower() == "id" and "INT" in attr_type.upper() else ""
                columns.append(f"`{name}` {attr_type}{auto_inc} PRIMARY KEY")
                pk_added = True
            else:
                columns.append(f"`{name}` {attr_type}")

        # Fallback if the class had no attributes defined in UML
        if not pk_added:
            columns.insert(0, f"`{pk_name}` {pk_info['type']} PRIMARY KEY")

        columns.extend(table_columns[class_name])

        table_sql = f"CREATE TABLE `{class_name}` (\n    " + ",\n    ".join(columns) + "\n);\n"
        sql_statements.append(table_sql)

    # ================================
    # STEP 3: CREATE JUNCTION TABLES
    # ================================
    if junction_tables:
        sql_statements.append("-- Junction Tables")
        sql_statements.extend(junction_tables)

    # ================================
    # STEP 4: ADD FOREIGN KEYS LAST
    # ================================
    if fk_constraints:
        sql_statements.append("-- Foreign Keys")
        sql_statements.extend(fk_constraints)

    # ================================
    # WRITE FILE
    # ================================
    with open(output_file, "w") as f:
        f.write("\n\n".join(sql_statements))

    print(f"Schema successfully generated and saved to {output_file}")
    return output_file