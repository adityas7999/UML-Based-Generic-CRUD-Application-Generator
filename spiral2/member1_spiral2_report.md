# Spiral 2 - Member 1 (Parit)

## Objective

Build a clean and reusable UML to MySQL type conversion module for Spiral 2.

## Scope Completed

- Implemented isolated type mapping module at `schema_generator/type_mapper.py`
- Added reusable function: `map_type(uml_type) -> mysql_type`
- Added unit tests at `tests/test_type_mapper.py`
- Added README contribution section for Spiral 2 Member 1

## Mapping Table

| UML Type | MySQL Type |
| --- | --- |
| String | VARCHAR(255) |
| Integer | INT |
| Boolean | TINYINT(1) |
| Float | DECIMAL(10,2) |
| Date | DATETIME |

Supported aliases in implementation: `int`, `double`, `datetime`.

## Risk Handling Implemented

- Unknown type defaults to `VARCHAR(255)`
- Empty/blank type defaults to `VARCHAR(255)`
- Warning logs are generated for unknown/empty/blank values
- Case-insensitive conversion by normalizing input type

## Input Example (Spiral 2)

```json
{
  "classes": [
    {
      "name": "Student",
      "attributes": [
        {"name": "name", "type": "String"},
        {"name": "age", "type": "Integer"}
      ]
    }
  ]
}
```

## Expected Schema Output Example

```sql
CREATE TABLE Student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT
);
```

## Member 1 Deliverable Status

- [x] `type_mapper.py` created
- [x] Mapping table implemented
- [x] Unknown type fallback implemented
- [x] Warning logging implemented
- [x] Case-insensitive mapping implemented
- [x] Unit tests for known, unknown, and case-insensitive inputs

## Notes

Primary key strategy, nullability, `CREATE TABLE` generation, and MySQL execution are intentionally outside Member 1 scope and are for Member 2/schema generator integration.
