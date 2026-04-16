"""
Auto-generated Repository Layer
Handles all database access and CRUD operations.
Uses parameterized queries for SQL injection safety.
"""

from typing import List, Dict, Any, Optional
from config import get_connection
# ============================================================================
# Student Repository Functions
# ============================================================================

def insert_student(name: Any) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO `Student` (                `name`            ) VALUES (                %s            )
        """
        params = (name, )
        
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"DATABASE ERROR in insert_student: {e}")
        return False


def get_all_student() -> Optional[List[Dict[str, Any]]]:
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT                `id`,                `name`            FROM `Student`
        """
        
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"DATABASE ERROR in get_all_student: {e}")
        return None


def get_student_by_id(id: Any) -> Optional[Dict[str, Any]]:
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT                `id`,                `name`            FROM `Student`
            WHERE `id` = %s
        """
        
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"DATABASE ERROR in get_student_by_id: {e}")
        return None


def update_student(id: Any, name: Any) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE `Student` 
            SET                `name` = %s            WHERE `id` = %s
        """
        params = (name, id,)
        
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"DATABASE ERROR in update_student: {e}")
        return False

def delete_student(id: Any) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM `Student` WHERE `id` = %s"
        
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"DATABASE ERROR in delete_student: {e}")
        return False
