"""
Central Database Configuration
All database operations in the application use connections from this module.
This centralizes connection management and prevents duplication across layers.
"""

import mysql.connector


def get_connection():
    """
    Get a fresh MySQL database connection.
    
    This is the ONLY place where database connections are created.
    All repository functions use this function to get their connection.
    
    Returns:
        mysql.connector.connection.MySQLConnection: A new database connection
    
    Raises:
        mysql.connector.Error: If connection to database fails
    
    Configuration:
        - host: Database server address
        - user: MySQL username
        - password: MySQL password
        - database: Database name
    
    Note:
        Each connection is independent. Callers are responsible for closing
        the connection after use.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # UPDATE: Replace with actual password
        database="uml_crud_db"
    )
