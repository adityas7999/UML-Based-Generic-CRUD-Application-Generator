"""
Auto-generated Repository Layer
Handles all database access and CRUD operations.
Uses parameterized queries for SQL injection safety.
"""

from typing import List, Dict, Any, Optional
from config import get_connection


# ============================================================================
# Course Repository Functions
# ============================================================================

def insert_course(courseId: Any, title: Any) -> bool:
    """
    Insert a new Course record into database.
    
    Args:
        courseId: int value
        title: string value
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO `course` (
                `courseId`,
                `title`
            ) VALUES (
                %s,
                %s
            )
        """
        params = (courseId,title,)
        
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def get_all_course() -> Optional[List[Dict[str, Any]]]:
    """
    Retrieve all Course records from database.
    
    Returns:
        List of Course records as dictionaries, or None on error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT `id`,
                `courseId`,
                `title`
            FROM `course`
        """
        
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception:
        return None


def get_course_by_id(id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single Course record by ID.
    
    Args:
        id: The primary key ID of Course
    
    Returns:
        Course record as dictionary, or None if not found/error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT `id`,
                `courseId`,
                `title`
            FROM `course`
            WHERE `id` = %s
        """
        
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception:
        return None


def update_course(id: int, courseId: Any, title: Any) -> bool:
    """
    Update a Course record in database.
    
    Args:
        id: The primary key ID of Course to update
        courseId: New int value
        title: New string value
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE `course` 
            SET
                `courseId` = %s,
                `title` = %s
            WHERE `id` = %s
        """
        params = (courseId,title, id,)
        
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def delete_course(id: int) -> bool:
    """
    Delete a Course record from database.
    
    Args:
        id: The primary key ID of Course to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM `course` WHERE `id` = %s"
        
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


# ============================================================================
# Department Repository Functions
# ============================================================================

def insert_department(deptId: Any, deptName: Any) -> bool:
    """
    Insert a new Department record into database.
    
    Args:
        deptId: int value
        deptName: string value
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO `department` (
                `deptId`,
                `deptName`
            ) VALUES (
                %s,
                %s
            )
        """
        params = (deptId,deptName,)
        
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def get_all_department() -> Optional[List[Dict[str, Any]]]:
    """
    Retrieve all Department records from database.
    
    Returns:
        List of Department records as dictionaries, or None on error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT `id`,
                `deptId`,
                `deptName`
            FROM `department`
        """
        
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception:
        return None


def get_department_by_id(id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single Department record by ID.
    
    Args:
        id: The primary key ID of Department
    
    Returns:
        Department record as dictionary, or None if not found/error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT `id`,
                `deptId`,
                `deptName`
            FROM `department`
            WHERE `id` = %s
        """
        
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception:
        return None


def update_department(id: int, deptId: Any, deptName: Any) -> bool:
    """
    Update a Department record in database.
    
    Args:
        id: The primary key ID of Department to update
        deptId: New int value
        deptName: New string value
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE `department` 
            SET
                `deptId` = %s,
                `deptName` = %s
            WHERE `id` = %s
        """
        params = (deptId,deptName, id,)
        
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def delete_department(id: int) -> bool:
    """
    Delete a Department record from database.
    
    Args:
        id: The primary key ID of Department to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM `department` WHERE `id` = %s"
        
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


# ============================================================================
# Enrollment Repository Functions
# ============================================================================

def insert_enrollment(enrollmentId: Any, status: Any) -> bool:
    """
    Insert a new Enrollment record into database.
    
    Args:
        enrollmentId: int value
        status: string value
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO `enrollment` (
                `enrollmentId`,
                `status`
            ) VALUES (
                %s,
                %s
            )
        """
        params = (enrollmentId,status,)
        
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def get_all_enrollment() -> Optional[List[Dict[str, Any]]]:
    """
    Retrieve all Enrollment records from database.
    
    Returns:
        List of Enrollment records as dictionaries, or None on error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT `id`,
                `enrollmentId`,
                `status`
            FROM `enrollment`
        """
        
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception:
        return None


def get_enrollment_by_id(id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single Enrollment record by ID.
    
    Args:
        id: The primary key ID of Enrollment
    
    Returns:
        Enrollment record as dictionary, or None if not found/error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT `id`,
                `enrollmentId`,
                `status`
            FROM `enrollment`
            WHERE `id` = %s
        """
        
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception:
        return None


def update_enrollment(id: int, enrollmentId: Any, status: Any) -> bool:
    """
    Update a Enrollment record in database.
    
    Args:
        id: The primary key ID of Enrollment to update
        enrollmentId: New int value
        status: New string value
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE `enrollment` 
            SET
                `enrollmentId` = %s,
                `status` = %s
            WHERE `id` = %s
        """
        params = (enrollmentId,status, id,)
        
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def delete_enrollment(id: int) -> bool:
    """
    Delete a Enrollment record from database.
    
    Args:
        id: The primary key ID of Enrollment to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM `enrollment` WHERE `id` = %s"
        
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


# ============================================================================
# Person Repository Functions
# ============================================================================

def insert_person(name: Any) -> bool:
    """
    Insert a new Person record into database.
    
    Args:
        name: string value
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO `person` (
                `name`
            ) VALUES (
                %s
            )
        """
        params = (name,)
        
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def get_all_person() -> Optional[List[Dict[str, Any]]]:
    """
    Retrieve all Person records from database.
    
    Returns:
        List of Person records as dictionaries, or None on error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT `id`,
                `name`
            FROM `person`
        """
        
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception:
        return None


def get_person_by_id(id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single Person record by ID.
    
    Args:
        id: The primary key ID of Person
    
    Returns:
        Person record as dictionary, or None if not found/error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT `id`,
                `name`
            FROM `person`
            WHERE `id` = %s
        """
        
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception:
        return None


def update_person(id: int, name: Any) -> bool:
    """
    Update a Person record in database.
    
    Args:
        id: The primary key ID of Person to update
        name: New string value
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE `person` 
            SET
                `name` = %s
            WHERE `id` = %s
        """
        params = (name, id,)
        
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def delete_person(id: int) -> bool:
    """
    Delete a Person record from database.
    
    Args:
        id: The primary key ID of Person to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM `person` WHERE `id` = %s"
        
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


# ============================================================================
# Professor Repository Functions
# ============================================================================

def insert_professor(employeeId: Any, specialization: Any) -> bool:
    """
    Insert a new Professor record into database.
    
    Args:
        employeeId: int value
        specialization: string value
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO `professor` (
                `employeeId`,
                `specialization`
            ) VALUES (
                %s,
                %s
            )
        """
        params = (employeeId,specialization,)
        
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def get_all_professor() -> Optional[List[Dict[str, Any]]]:
    """
    Retrieve all Professor records from database.
    
    Returns:
        List of Professor records as dictionaries, or None on error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT `id`,
                `employeeId`,
                `specialization`
            FROM `professor`
        """
        
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception:
        return None


def get_professor_by_id(id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single Professor record by ID.
    
    Args:
        id: The primary key ID of Professor
    
    Returns:
        Professor record as dictionary, or None if not found/error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT `id`,
                `employeeId`,
                `specialization`
            FROM `professor`
            WHERE `id` = %s
        """
        
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception:
        return None


def update_professor(id: int, employeeId: Any, specialization: Any) -> bool:
    """
    Update a Professor record in database.
    
    Args:
        id: The primary key ID of Professor to update
        employeeId: New int value
        specialization: New string value
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE `professor` 
            SET
                `employeeId` = %s,
                `specialization` = %s
            WHERE `id` = %s
        """
        params = (employeeId,specialization, id,)
        
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def delete_professor(id: int) -> bool:
    """
    Delete a Professor record from database.
    
    Args:
        id: The primary key ID of Professor to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM `professor` WHERE `id` = %s"
        
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


# ============================================================================
# Student Repository Functions
# ============================================================================

def insert_student(rollNumber: Any, enrollmentDate: Any) -> bool:
    """
    Insert a new Student record into database.
    
    Args:
        rollNumber: int value
        enrollmentDate: date value
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO `student` (
                `rollNumber`,
                `enrollmentDate`
            ) VALUES (
                %s,
                %s
            )
        """
        params = (rollNumber,enrollmentDate,)
        
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def get_all_student() -> Optional[List[Dict[str, Any]]]:
    """
    Retrieve all Student records from database.
    
    Returns:
        List of Student records as dictionaries, or None on error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT `id`,
                `rollNumber`,
                `enrollmentDate`
            FROM `student`
        """
        
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception:
        return None


def get_student_by_id(id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single Student record by ID.
    
    Args:
        id: The primary key ID of Student
    
    Returns:
        Student record as dictionary, or None if not found/error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT `id`,
                `rollNumber`,
                `enrollmentDate`
            FROM `student`
            WHERE `id` = %s
        """
        
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception:
        return None


def update_student(id: int, rollNumber: Any, enrollmentDate: Any) -> bool:
    """
    Update a Student record in database.
    
    Args:
        id: The primary key ID of Student to update
        rollNumber: New int value
        enrollmentDate: New date value
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE `student` 
            SET
                `rollNumber` = %s,
                `enrollmentDate` = %s
            WHERE `id` = %s
        """
        params = (rollNumber,enrollmentDate, id,)
        
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def delete_student(id: int) -> bool:
    """
    Delete a Student record from database.
    
    Args:
        id: The primary key ID of Student to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM `student` WHERE `id` = %s"
        
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False
