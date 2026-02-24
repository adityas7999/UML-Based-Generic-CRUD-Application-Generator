import sys
import json
from parser import parse_xmi
from validator import validate_model


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

    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()