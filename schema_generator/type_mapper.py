import logging

LOGGER = logging.getLogger(__name__)

DEFAULT_MYSQL_TYPE = "VARCHAR(255)"

UML_TO_MYSQL_TYPE_MAP = {
    "string": "VARCHAR(255)",
    "integer": "INT",
    "int": "INT",
    "boolean": "TINYINT(1)",
    "float": "DECIMAL(10,2)",
    "double": "DECIMAL(10,2)",
    "date": "DATETIME",
    "datetime": "DATETIME",
}


def map_type(uml_type: str) -> str:
    """Convert a UML data type to a MySQL data type."""

    if uml_type is None:
        LOGGER.warning("Empty UML type received. Defaulting to %s", DEFAULT_MYSQL_TYPE)
        return DEFAULT_MYSQL_TYPE

    normalized_type = str(uml_type).strip().lower()

    if not normalized_type:
        LOGGER.warning("Blank UML type received. Defaulting to %s", DEFAULT_MYSQL_TYPE)
        return DEFAULT_MYSQL_TYPE

    mysql_type = UML_TO_MYSQL_TYPE_MAP.get(normalized_type)
    if mysql_type:
        return mysql_type

    LOGGER.warning("Unknown UML type '%s'. Defaulting to %s", uml_type, DEFAULT_MYSQL_TYPE)
    return DEFAULT_MYSQL_TYPE