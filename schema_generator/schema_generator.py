import os
from schema_generator.type_mapper import map_type

def generate_schema(model_data, output_file="schema.sql", db_name="uml_crud_db"):
    """
    Converts parsed UML model data into a MySQL schema.sql file.
    Automatically includes database creation commands and Spiral 3 Foreign Key relationships.
    """
    sql_statements = [
        f"CREATE DATABASE IF NOT EXISTS `{db_name}`;",
        f"USE `{db_name}`;\n"
    ]
    
    classes = model_data
    associations = []
    
    if isinstance(model_data, dict):
        if "classes" in model_data:
            classes = model_data["classes"]
        if "associations" in model_data:
            associations = model_data["associations"]

    # --- SPIRAL 3: PRE-CALCULATE FOREIGN KEYS ---
    table_fks = {}
    
    for assoc in associations:
        source = assoc.get("source")
        target = assoc.get("target")
        
        # 🛡️ TWEAK 3: DEFENSIVE PARSING
        if not source or not target:
            print(f"⚠️ Warning: Skipping malformed association: {assoc}")
            continue

        rel_type = assoc.get("type", "").lower()

        if rel_type in ["many-to-one", "1:*", "one-to-many", "1:1", "one-to-one"]:
            child_table = source 
            parent_table = target
            
            fk_col_name = f"{parent_table.lower()}_id"
            
            # ✍️ BUG FIX: Bundle the comment with the column definition so the comma doesn't break
            fk_col_def = f"    -- Foreign Key linking to {parent_table}\n    `{fk_col_name}` INT"
            fk_const_def = f"    FOREIGN KEY (`{fk_col_name}`) REFERENCES `{parent_table}`(`id`)"
            
            if child_table not in table_fks:
                table_fks[child_table] = []
            table_fks[child_table].append((fk_col_def, fk_const_def))

    # --- GENERATE TABLES ---
    for class_name, attributes in classes.items():
        
        table_sql = f"CREATE TABLE `{class_name}` (\n"
        columns = ["    `id` INT AUTO_INCREMENT PRIMARY KEY"]
        
        for attr in attributes:
            attr_name = attr.get("name")
            attr_type = attr.get("type")
            
            if attr_name and attr_name.lower() == "id":
                continue
                
            mysql_type = map_type(attr_type)
            columns.append(f"    `{attr_name}` {mysql_type}")
            
        # --- SPIRAL 3: INJECT FOREIGN KEYS ---
        if class_name in table_fks:
            for fk_col, fk_const in table_fks[class_name]:
                columns.append(fk_col)
                columns.append(fk_const)
            
        table_sql += ",\n".join(columns)
        table_sql += "\n);\n"
        
        sql_statements.append(table_sql)

    with open(output_file, "w") as f:
        f.write("\n".join(sql_statements))
        
    print(f"Schema successfully generated and saved to {output_file}")
    
    return output_file