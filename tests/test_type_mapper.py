from schema_generator.type_mapper import map_type


def test_known_types():
    assert map_type("String") == "VARCHAR(255)"
    assert map_type("Integer") == "INT"
    assert map_type("Boolean") == "TINYINT(1)"
    assert map_type("Float") == "DECIMAL(10,2)"
    assert map_type("Date") == "DATETIME"


def test_case_insensitivity():
    assert map_type("string") == "VARCHAR(255)"
    assert map_type("INTEGER") == "INT"
    assert map_type("BoOlEaN") == "TINYINT(1)"


def test_unknown_type_defaults_to_varchar():
    assert map_type("CustomType") == "VARCHAR(255)"


def test_empty_or_none_defaults_to_varchar():
    assert map_type("") == "VARCHAR(255)"
    assert map_type("   ") == "VARCHAR(255)"
    assert map_type(None) == "VARCHAR(255)"