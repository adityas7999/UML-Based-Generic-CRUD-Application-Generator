"""
Member 2 - Repository Layer Generator
USAGE EXAMPLES AND DOCUMENTATION

This module demonstrates how to use the auto-generated repository.py
for database CRUD operations.
"""

# ============================================================================
# EXAMPLE 1: Initialize Database Connection
# ============================================================================

from generated_app.repository import get_db, init_db, close_db

# Initialize database (call this once at application startup)
success = init_db(
    host="localhost",
    user="root",
    password="",
    database="uml_crud_db"
)

if not success:
    print("Failed to connect to database")
    exit(1)

print("✓ Database connection established")


# ============================================================================
# EXAMPLE 2: CREATE (INSERT)
# ============================================================================

from generated_app.repository import (
    insert_student, 
    insert_course,
    insert_department
)

# Insert a new Student
success = insert_student(
    name="Alice Johnson",
    rollNumber=101,
    enrollmentDate="2024-01-15"
)
print(f"✓ Student created: {success}")

# Insert a Course
success = insert_course(
    title="Data Structures",
    courseId=1001
)
print(f"✓ Course created: {success}")

# Insert a Department
success = insert_department(
    deptName="Computer Science",
    deptId=10
)
print(f"✓ Department created: {success}")


# ============================================================================
# EXAMPLE 3: READ (SELECT)
# ============================================================================

from generated_app.repository import (
    get_all_student,
    get_student_by_id,
    get_all_course,
    get_course_by_id
)

# Get ALL students
all_students = get_all_student()
print(f"\n📚 All Students: {all_students}")

# Get ALL courses
all_courses = get_all_course()
print(f"📚 All Courses: {all_courses}")

# Get specific student by ID
student_1 = get_student_by_id(1)
print(f"👤 Student with ID 1: {student_1}")

# Get specific course by ID
course_1 = get_course_by_id(1)
print(f"📖 Course with ID 1: {course_1}")


# ============================================================================
# EXAMPLE 4: UPDATE (MODIFY)
# ============================================================================

from generated_app.repository import (
    update_student,
    update_course
)

# Update student information
success = update_student(
    id=1,
    name="Alice Johnson Updated",
    rollNumber=102,
    enrollmentDate="2024-02-20"
)
print(f"\n✓ Student updated: {success}")

# Update course information
success = update_course(
    id=1,
    title="Advanced Data Structures",
    courseId=1002
)
print(f"✓ Course updated: {success}")


# ============================================================================
# EXAMPLE 5: DELETE (REMOVE)
# ============================================================================

from generated_app.repository import (
    delete_student,
    delete_course
)

# Delete a student by ID
success = delete_student(id=5)
print(f"\n🗑️  Student deleted: {success}")

# Delete a course by ID
success = delete_course(id=3)
print(f"🗑️  Course deleted: {success}")


# ============================================================================
# EXAMPLE 6: COMPLETE CRUD WORKFLOW
# ============================================================================

print("\n" + "="*70)
print("COMPLETE CRUD WORKFLOW EXAMPLE")
print("="*70)

# 1. CREATE
print("\n1. CREATE - Insert new records")
insert_student(name="Bob Smith")
insert_student(name="Carol White")
insert_course(title="Database Design")
print("   ✓ Records created")

# 2. READ
print("\n2. READ - Fetch all records")
students = get_all_student()
courses = get_all_course()
print(f"   ✓ {len(students)} students found")
print(f"   ✓ {len(courses)} courses found")

# 3. UPDATE
print("\n3. UPDATE - Modify records")
update_student(id=1, name="Bob Smith Updated")
print("   ✓ Student record updated")

# 4. DELETE
print("\n4. DELETE - Remove records")
delete_student(id=3)
print("   ✓ Student record deleted")

# 5. VERIFY
print("\n5. VERIFY - Check final state")
final_students = get_all_student()
print(f"   ✓ Final student count: {len(final_students)}")


# ============================================================================
# EXAMPLE 7: ERROR HANDLING
# ============================================================================

print("\n" + "="*70)
print("ERROR HANDLING EXAMPLES")
print("="*70)

# The repository functions handle errors internally
# If a query fails, it returns False (for insert/update/delete)
# or None (for select queries)

# Try to insert with empty name (may fail depending on DB constraints)
result = insert_student(name="")
if result:
    print("✓ Record inserted")
else:
    print("✗ Insert failed (DB constraint or connection error)")

# Try to get non-existent record
result = get_student_by_id(999999)
if result:
    print(f"✓ Record found: {result}")
else:
    print("✗ Record not found or query error")


# ============================================================================
# EXAMPLE 8: DATABASE CONNECTION CLEANUP
# ============================================================================

print("\n" + "="*70)
print("CLEANUP")
print("="*70)

# Close database connection (call this at application shutdown)
close_db()
print("✓ Database connection closed")


# ============================================================================
# KEY FEATURES OF GENERATED REPOSITORY
# ============================================================================

"""
✓ PARAMETERIZED QUERIES
  - Protection against SQL injection
  - Parameters are properly escaped by MySQL connector
  - Format: cursor.execute("SELECT * FROM table WHERE id = %s", (id,))

✓ SINGLETON DATABASE CONNECTION
  - DatabaseConnection class uses singleton pattern
  - get_db() always returns the same instance
  - Efficient connection reuse

✓ ERROR HANDLING
  - Try-catch blocks in all methods
  - Returns False for failed operations
  - Returns None for failed SELECT queries
  - Error messages are printed to console

✓ TYPE HINTS
  - All function signatures include type hints
  - Better IDE autocomplete and type checking
  - Improved code documentation

✓ DETERMINISTIC GENERATION
  - Classes are sorted alphabetically
  - Same UML model → Same repository.py
  - Reproducible outputs for version control

✓ STANDARD CRUD OPERATIONS
  - insert_<class>() - CREATE
  - get_all_<class>() - READ ALL
  - get_<class>_by_id(id) - READ ONE
  - update_<class>(id, ...) - UPDATE
  - delete_<class>(id) - DELETE

✓ MYSQL CONNECTOR
  - Uses mysql-connector-python
  - Returns results as dictionaries
  - Automatic commit/rollback handling
"""


# ============================================================================
# GENERATED FUNCTION SIGNATURES
# ============================================================================

"""
For a class named "Student" with attributes [name, age, email]:

def insert_student(name: Any, age: Any, email: Any) -> bool:
    '''Insert a new Student record.'''

def get_all_student() -> Optional[List[Dict[str, Any]]]:
    '''Retrieve all Student records.'''

def get_student_by_id(id: int) -> Optional[Dict[str, Any]]:
    '''Retrieve a single Student by ID.'''

def update_student(id: int, name: Any, age: Any, email: Any) -> bool:
    '''Update a Student record.'''

def delete_student(id: int) -> bool:
    '''Delete a Student record.'''
"""
