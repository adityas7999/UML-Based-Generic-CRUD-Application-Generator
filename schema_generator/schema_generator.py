import os
from schema_generator.type_mapper import map_type

def generate_schema(model_data, output_file="schema.sql", db_name="uml_crud_db"):
    """
    Converts parsed UML model data into a MySQL schema.sql file.
    Automatically includes database creation commands and Spiral 3 Foreign Key relationships.
    """
    sql_statements = [
        f"CREATE DATABASE IF NOT EXISTS {db_name};",
        f"USE {db_name};\n"
    ]
    
    classes = model_data
    associations = []
    
    # Extract classes and the new associations array from Member 1's JSON
    if isinstance(model_data, dict):
        if "classes" in model_data:
            classes = model_data["classes"]
        if "associations" in model_data:
            associations = model_data["associations"]

    # --- SPIRAL 3: PRE-CALCULATE FOREIGN KEYS ---
    # Map out which table gets which foreign keys: { "ChildTable": [("col_def", "constraint_def")] }
    table_fks = {}
    
    for assoc in associations:
        source = assoc.get("source")
        target = assoc.get("target")
        rel_type = assoc.get("type", "").lower()

        # In a 1:* or many-to-one, the "many" side (source) holds the foreign key to the "one" side (target).
        # Catching Member 1's specific naming conventions
        if rel_type in ["many-to-one", "1:*", "one-to-many", "1:1", "one-to-one"]:
            child_table = source 
            parent_table = target
            
            # Adhering to the Integration Lead's naming rule: <Class>_id
            fk_col_name = f"{parent_table.lower()}_id"
            fk_col_def = f"    {fk_col_name} INT"
            fk_const_def = f"    FOREIGN KEY ({fk_col_name}) REFERENCES {parent_table}(id)"
            
            if child_table not in table_fks:
                table_fks[child_table] = []
            table_fks[child_table].append((fk_col_def, fk_const_def))

    # --- GENERATE TABLES ---
    # Iterate over the dictionary of classes and their attributes
    for class_name, attributes in classes.items():
        
        # Start the CREATE TABLE statement
        table_sql = f"CREATE TABLE {class_name} (\n"
        
        # Inject the mandatory primary key as required by Spiral 2
        columns = ["    id INT AUTO_INCREMENT PRIMARY KEY"]
        
        # Process each attribute from the UML
        for attr in attributes:
            attr_name = attr.get("name")
            attr_type = attr.get("type")
            
            # Skip if the UML already has an 'id' attribute to prevent duplicate primary keys
            if attr_name and attr_name.lower() == "id":
                continue
                
            # Map the UML data type to MySQL data type using Member 1's logic
            mysql_type = map_type(attr_type)
            
            # Add to the columns list
            columns.append(f"    {attr_name} {mysql_type}")
            
        # --- SPIRAL 3: INJECT FOREIGN KEYS ---
        # If this class was identified as a child table earlier, add its FKs
        if class_name in table_fks:
            for fk_col, fk_const in table_fks[class_name]:
                columns.append(fk_col)
                columns.append(fk_const)
            
        # Join columns with a comma and newline (this guarantees NO trailing commas)
        table_sql += ",\n".join(columns)
        table_sql += "\n);\n"
        
        sql_statements.append(table_sql)

    # Write the complete SQL script to the output file
    with open(output_file, "w") as f:
        f.write("\n".join(sql_statements))
        
    print(f"Schema successfully generated and saved to {output_file}")
    
    return output_file