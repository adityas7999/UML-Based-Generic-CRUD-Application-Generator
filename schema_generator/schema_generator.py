import os
from schema_generator.type_mapper import map_type

def generate_schema(model_data, output_file="schema.sql", db_name="uml_crud_db"):
    """
    Converts parsed UML model data into a MySQL schema.sql file.
    Refined for Spiral 3: Handles 1:1 (Unique), Many-to-Many (Junction Tables), 
    and Deterministic Output.
    """
    sql_statements = [
        f"CREATE DATABASE IF NOT EXISTS `{db_name}`;",
        f"USE `{db_name}`;\n"
    ]
    
    classes_dict = {}
    associations = []
    
    if isinstance(model_data, dict):
        classes_dict = model_data.get("classes", {})
        associations = model_data.get("associations", [])

    # 🔧 5. ENSURE DETERMINISTIC OUTPUT (Sort classes and associations)
    sorted_class_names = sorted(classes_dict.keys())
    # Sort associations by source, then target for consistency
    sorted_associations = sorted(associations, key=lambda x: (x.get("source", ""), x.get("target", "")))

    # --- SPIRAL 3: PRE-CALCULATE FOREIGN KEYS & JUNCTION TABLES ---
    table_fks = {name: [] for name in sorted_class_names}
    junction_tables = []
    
    # 🔧 4. PREVENT DUPLICATE FK COLUMNS tracker
    added_fk_columns = {name: set() for name in sorted_class_names}

    for assoc in sorted_associations:
        source = assoc.get("source")
        target = assoc.get("target")
        rel_type = assoc.get("type", "").lower()
        
        # 🔧 6. HANDLE SELF-RELATION (Edge Case)
        is_self_relation = (source == target)

        if not source or not target:
            continue

        # 🔧 2. FIX FK PLACEMENT LOGIC (BASED ON TYPE)
        if rel_type == "many-to-many":
            # 🔧 1. ADD MANY-TO-MANY HANDLING (Junction Table)
            # Alphabetical sorting for junction table name (e.g., Course_Student)
            sorted_pair = sorted([source, target])
            j_table_name = f"{sorted_pair[0]}_{sorted_pair[1]}"
            
            # Use specific names for self-relation in junction tables
            col1 = f"{source.lower()}_id_1" if is_self_relation else f"{source.lower()}_id"
            col2 = f"{target.lower()}_id_2" if is_self_relation else f"{target.lower()}_id"
            
            junction_sql = f"CREATE TABLE `{j_table_name}` (\n"
            junction_sql += f"    `{col1}` INT,\n"
            junction_sql += f"    `{col2}` INT,\n"
            junction_sql += f"    FOREIGN KEY (`{col1}`) REFERENCES `{source}`(`id`),\n"
            junction_sql += f"    FOREIGN KEY (`{col2}`) REFERENCES `{target}`(`id`)\n"
            junction_sql += ");"
            
            if junction_sql not in junction_tables:
                junction_tables.append(junction_sql)
            continue

        # FK Placement Logic
        child_table = None
        parent_table = None
        is_unique = False

        if rel_type == "one-to-many":
            child_table = target # "Many" side is target
            parent_table = source
        elif rel_type == "many-to-one":
            child_table = source # "Many" side is source
            parent_table = target
        elif rel_type in ["one-to-one", "1:1"]:
            child_table = source # Fixed rule: source gets FK
            parent_table = target
            is_unique = True # 🔧 3. IMPROVE ONE-TO-ONE (UNIQUE)

        if child_table and parent_table and child_table in table_fks:
            fk_col_name = f"{parent_table.lower()}_id"
            
            # Handling self-relation column name conflict
            if is_self_relation:
                fk_col_name = f"parent_{fk_col_name}"

            # 🔧 4. PREVENT DUPLICATE FK COLUMNS
            if fk_col_name in added_fk_columns[child_table]:
                continue
            
            added_fk_columns[child_table].add(fk_col_name)

            unique_str = " UNIQUE" if is_unique else ""
            fk_col_def = f"    -- Foreign Key linking to {parent_table}\n    `{fk_col_name}` INT{unique_str}"
            fk_const_def = f"    FOREIGN KEY (`{fk_col_name}`) REFERENCES `{parent_table}`(`id`)"
            
            table_fks[child_table].append((fk_col_def, fk_const_def))

    # --- GENERATE TABLES ---
    for class_name in sorted_class_names:
        attributes = classes_dict[class_name]
        table_sql = f"CREATE TABLE `{class_name}` (\n"
        columns = ["    `id` INT AUTO_INCREMENT PRIMARY KEY"]
        
        for attr in attributes:
            attr_name = attr.get("name")
            if not attr_name or attr_name.lower() == "id":
                continue
            mysql_type = map_type(attr.get("type"))
            columns.append(f"    `{attr_name}` {mysql_type}")
            
        # Inject Foreign Keys
        if class_name in table_fks:
            for fk_col, fk_const in table_fks[class_name]:
                columns.append(fk_col)
                columns.append(fk_const)
            
        table_sql += ",\n".join(columns)
        table_sql += "\n);\n"
        sql_statements.append(table_sql)

    # Append Junction Tables at the end
    if junction_tables:
        sql_statements.append("-- Many-to-Many Junction Tables")
        sql_statements.extend(junction_tables)

    with open(output_file, "w") as f:
        f.write("\n\n".join(sql_statements))
        
    print(f"Schema successfully generated and saved to {output_file}")
    return output_file