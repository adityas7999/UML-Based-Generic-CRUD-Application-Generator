import os
from schema_generator.type_mapper import map_type

def generate_schema(model_data, output_file="schema.sql", db_name="uml_crud_db"):
    """
    Converts parsed UML model data into a MySQL schema.sql file.
    Automatically includes database creation commands.
    """
    # START CHANGE: Add the CREATE DATABASE and USE commands at the top
    sql_statements = [
        f"CREATE DATABASE IF NOT EXISTS {db_name};",
        f"USE {db_name};\n"
    ]
    # END CHANGE
    # Iterate over the dictionary of classes and their attributes
    for class_name, attributes in model_data.items():
        
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
            
        # Join columns with a comma and newline (this guarantees NO trailing commas)
        table_sql += ",\n".join(columns)
        table_sql += "\n);\n"
        
        sql_statements.append(table_sql)

    # Write the complete SQL script to the output file
    with open(output_file, "w") as f:
        f.write("\n".join(sql_statements))
        
    print(f"Schema successfully generated and saved to {output_file}")
    
    return output_file
