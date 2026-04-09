import sys
import json
from parser import parse_xmi
from validator import validate_model
from schema_generator.schema_generator import generate_schema
from code_generator.model_generator import generate_models
from code_generator.repository_generator import generate_repository

def main():

    if len(sys.argv) != 2:
        print("Usage: python generate.py <input.xmi>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        print(f"Parsing: {input_file}")
        parsed_data = parse_xmi(input_file)

        print("Validating model...")
        validated_data = validate_model(parsed_data)

        print("Model parsed successfully!\n")
        print(json.dumps(validated_data, indent=4))

        print("\n" + "="*70)
        print("Generating SQL Schema...")
        output_sql_file = generate_schema(validated_data, "schema.sql")

        print("Generating Python models...")
        output_models_file = generate_models(validated_data, "generated_app/models.py")

        print("Generating Repository layer...")
        output_repository_file = generate_repository(validated_data, "generated_app/repository.py")

        print("="*70)
        print("\nPipeline Complete! Backend components generated:\n")
        print(f"  ✓ Database Schema:  {output_sql_file}")
        print(f"  ✓ Model Classes:    {output_models_file}")
        print(f"  ✓ Repository Layer: {output_repository_file}")
        print("\nNext steps:")
        print("  1. Run: mysql -u root -p < schema.sql")
        print("  2. Review generated_app/repository.py")
        print("  3. Configure database credentials in code")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()