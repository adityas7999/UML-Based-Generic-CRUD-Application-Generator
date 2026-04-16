from flask import Flask, request, jsonify
from flasgger import Swagger
from repository import *

app = Flask(__name__)

# Initialize Swagger for Auto-Documentation
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
swagger = Swagger(app, config=swagger_config, template={
    "info": {
        "title": "Auto-Generated MDE API",
        "description": "This REST API was completely auto-generated from a UML Class Diagram.",
        "version": "1.0.0"
    }
})


# ==========================================
# Person API Endpoints
# ==========================================

@app.route('/person', methods=['POST'])
def create_person_api():
    """
    Create a new Person
    ---
    tags:
      - Person
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Person
          required:
            
            - id
            
            - name
            
          properties:
            
            id:
              type: string
            
            name:
              type: string
            
    responses:
      201:
        description: Person created successfully
      400:
        description: Bad Request - Missing fields
      500:
        description: Internal Server Error
    """
    data = request.get_json()
    
    # 1. Bulletproof Error Handling: Dynamic Missing Field Check
    required_fields = ['id', 'name']
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Bad Request. Missing required fields: {', '.join(missing)}"}), 400

    try:
        create_person(data)
        return jsonify({"message": "Person created successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/person', methods=['GET'])
def get_all_person_api():
    """
    Get all Person records
    ---
    tags:
      - Person
    responses:
      200:
        description: A list of Person
      500:
        description: Internal Server Error
    """
    try:
        data = get_all_person()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/person/<int:id>', methods=['GET'])
def get_person_api(id):
    """
    Get a specific Person by ID
    ---
    tags:
      - Person
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the Person
    responses:
      200:
        description: Person data returned
      404:
        description: Person not found
    """
    try:
        data = get_person_by_id(id)
        if data:
            return jsonify(data), 200
        return jsonify({"error": "Person not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/person/<int:id>', methods=['PUT'])
def update_person_api(id):
    """
    Update an existing Person
    ---
    tags:
      - Person
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          id: PersonUpdate
    responses:
      200:
        description: Person updated
      404:
        description: Person not found
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided to update"}), 400
        
    try:
        # Assuming your repo returns True/False or rows affected
        update_person(id, data)
        return jsonify({"message": "Person updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Update failed: {str(e)}"}), 500


@app.route('/person/<int:id>', methods=['DELETE'])
def delete_person_api(id):
    """
    Delete a Person
    ---
    tags:
      - Person
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Person deleted
      404:
        description: Person not found
    """
    try:
        delete_person(id)
        return jsonify({"message": "Person deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Delete failed: {str(e)}"}), 500


# ==========================================
# Student API Endpoints
# ==========================================

@app.route('/student', methods=['POST'])
def create_student_api():
    """
    Create a new Student
    ---
    tags:
      - Student
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Student
          required:
            
            - rollNumber
            
            - enrollmentDate
            
          properties:
            
            rollNumber:
              type: string
            
            enrollmentDate:
              type: string
            
    responses:
      201:
        description: Student created successfully
      400:
        description: Bad Request - Missing fields
      500:
        description: Internal Server Error
    """
    data = request.get_json()
    
    # 1. Bulletproof Error Handling: Dynamic Missing Field Check
    required_fields = ['rollNumber', 'enrollmentDate']
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Bad Request. Missing required fields: {', '.join(missing)}"}), 400

    try:
        create_student(data)
        return jsonify({"message": "Student created successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/student', methods=['GET'])
def get_all_student_api():
    """
    Get all Student records
    ---
    tags:
      - Student
    responses:
      200:
        description: A list of Student
      500:
        description: Internal Server Error
    """
    try:
        data = get_all_student()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/student/<int:id>', methods=['GET'])
def get_student_api(id):
    """
    Get a specific Student by ID
    ---
    tags:
      - Student
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the Student
    responses:
      200:
        description: Student data returned
      404:
        description: Student not found
    """
    try:
        data = get_student_by_id(id)
        if data:
            return jsonify(data), 200
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/student/<int:id>', methods=['PUT'])
def update_student_api(id):
    """
    Update an existing Student
    ---
    tags:
      - Student
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          id: StudentUpdate
    responses:
      200:
        description: Student updated
      404:
        description: Student not found
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided to update"}), 400
        
    try:
        # Assuming your repo returns True/False or rows affected
        update_student(id, data)
        return jsonify({"message": "Student updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Update failed: {str(e)}"}), 500


@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student_api(id):
    """
    Delete a Student
    ---
    tags:
      - Student
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Student deleted
      404:
        description: Student not found
    """
    try:
        delete_student(id)
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Delete failed: {str(e)}"}), 500


# ==========================================
# Professor API Endpoints
# ==========================================

@app.route('/professor', methods=['POST'])
def create_professor_api():
    """
    Create a new Professor
    ---
    tags:
      - Professor
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Professor
          required:
            
            - employeeId
            
            - specialization
            
          properties:
            
            employeeId:
              type: string
            
            specialization:
              type: string
            
    responses:
      201:
        description: Professor created successfully
      400:
        description: Bad Request - Missing fields
      500:
        description: Internal Server Error
    """
    data = request.get_json()
    
    # 1. Bulletproof Error Handling: Dynamic Missing Field Check
    required_fields = ['employeeId', 'specialization']
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Bad Request. Missing required fields: {', '.join(missing)}"}), 400

    try:
        create_professor(data)
        return jsonify({"message": "Professor created successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/professor', methods=['GET'])
def get_all_professor_api():
    """
    Get all Professor records
    ---
    tags:
      - Professor
    responses:
      200:
        description: A list of Professor
      500:
        description: Internal Server Error
    """
    try:
        data = get_all_professor()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/professor/<int:id>', methods=['GET'])
def get_professor_api(id):
    """
    Get a specific Professor by ID
    ---
    tags:
      - Professor
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the Professor
    responses:
      200:
        description: Professor data returned
      404:
        description: Professor not found
    """
    try:
        data = get_professor_by_id(id)
        if data:
            return jsonify(data), 200
        return jsonify({"error": "Professor not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/professor/<int:id>', methods=['PUT'])
def update_professor_api(id):
    """
    Update an existing Professor
    ---
    tags:
      - Professor
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          id: ProfessorUpdate
    responses:
      200:
        description: Professor updated
      404:
        description: Professor not found
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided to update"}), 400
        
    try:
        # Assuming your repo returns True/False or rows affected
        update_professor(id, data)
        return jsonify({"message": "Professor updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Update failed: {str(e)}"}), 500


@app.route('/professor/<int:id>', methods=['DELETE'])
def delete_professor_api(id):
    """
    Delete a Professor
    ---
    tags:
      - Professor
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Professor deleted
      404:
        description: Professor not found
    """
    try:
        delete_professor(id)
        return jsonify({"message": "Professor deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Delete failed: {str(e)}"}), 500


# ==========================================
# Course API Endpoints
# ==========================================

@app.route('/course', methods=['POST'])
def create_course_api():
    """
    Create a new Course
    ---
    tags:
      - Course
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Course
          required:
            
            - courseId
            
            - title
            
          properties:
            
            courseId:
              type: string
            
            title:
              type: string
            
    responses:
      201:
        description: Course created successfully
      400:
        description: Bad Request - Missing fields
      500:
        description: Internal Server Error
    """
    data = request.get_json()
    
    # 1. Bulletproof Error Handling: Dynamic Missing Field Check
    required_fields = ['courseId', 'title']
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Bad Request. Missing required fields: {', '.join(missing)}"}), 400

    try:
        create_course(data)
        return jsonify({"message": "Course created successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/course', methods=['GET'])
def get_all_course_api():
    """
    Get all Course records
    ---
    tags:
      - Course
    responses:
      200:
        description: A list of Course
      500:
        description: Internal Server Error
    """
    try:
        data = get_all_course()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/course/<int:id>', methods=['GET'])
def get_course_api(id):
    """
    Get a specific Course by ID
    ---
    tags:
      - Course
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the Course
    responses:
      200:
        description: Course data returned
      404:
        description: Course not found
    """
    try:
        data = get_course_by_id(id)
        if data:
            return jsonify(data), 200
        return jsonify({"error": "Course not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/course/<int:id>', methods=['PUT'])
def update_course_api(id):
    """
    Update an existing Course
    ---
    tags:
      - Course
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          id: CourseUpdate
    responses:
      200:
        description: Course updated
      404:
        description: Course not found
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided to update"}), 400
        
    try:
        # Assuming your repo returns True/False or rows affected
        update_course(id, data)
        return jsonify({"message": "Course updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Update failed: {str(e)}"}), 500


@app.route('/course/<int:id>', methods=['DELETE'])
def delete_course_api(id):
    """
    Delete a Course
    ---
    tags:
      - Course
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Course deleted
      404:
        description: Course not found
    """
    try:
        delete_course(id)
        return jsonify({"message": "Course deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Delete failed: {str(e)}"}), 500


# ==========================================
# Department API Endpoints
# ==========================================

@app.route('/department', methods=['POST'])
def create_department_api():
    """
    Create a new Department
    ---
    tags:
      - Department
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Department
          required:
            
            - deptId
            
            - deptName
            
          properties:
            
            deptId:
              type: string
            
            deptName:
              type: string
            
    responses:
      201:
        description: Department created successfully
      400:
        description: Bad Request - Missing fields
      500:
        description: Internal Server Error
    """
    data = request.get_json()
    
    # 1. Bulletproof Error Handling: Dynamic Missing Field Check
    required_fields = ['deptId', 'deptName']
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Bad Request. Missing required fields: {', '.join(missing)}"}), 400

    try:
        create_department(data)
        return jsonify({"message": "Department created successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/department', methods=['GET'])
def get_all_department_api():
    """
    Get all Department records
    ---
    tags:
      - Department
    responses:
      200:
        description: A list of Department
      500:
        description: Internal Server Error
    """
    try:
        data = get_all_department()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/department/<int:id>', methods=['GET'])
def get_department_api(id):
    """
    Get a specific Department by ID
    ---
    tags:
      - Department
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the Department
    responses:
      200:
        description: Department data returned
      404:
        description: Department not found
    """
    try:
        data = get_department_by_id(id)
        if data:
            return jsonify(data), 200
        return jsonify({"error": "Department not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/department/<int:id>', methods=['PUT'])
def update_department_api(id):
    """
    Update an existing Department
    ---
    tags:
      - Department
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          id: DepartmentUpdate
    responses:
      200:
        description: Department updated
      404:
        description: Department not found
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided to update"}), 400
        
    try:
        # Assuming your repo returns True/False or rows affected
        update_department(id, data)
        return jsonify({"message": "Department updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Update failed: {str(e)}"}), 500


@app.route('/department/<int:id>', methods=['DELETE'])
def delete_department_api(id):
    """
    Delete a Department
    ---
    tags:
      - Department
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Department deleted
      404:
        description: Department not found
    """
    try:
        delete_department(id)
        return jsonify({"message": "Department deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Delete failed: {str(e)}"}), 500


# ==========================================
# Enrollment API Endpoints
# ==========================================

@app.route('/enrollment', methods=['POST'])
def create_enrollment_api():
    """
    Create a new Enrollment
    ---
    tags:
      - Enrollment
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Enrollment
          required:
            
            - enrollmentId
            
            - status
            
          properties:
            
            enrollmentId:
              type: string
            
            status:
              type: string
            
    responses:
      201:
        description: Enrollment created successfully
      400:
        description: Bad Request - Missing fields
      500:
        description: Internal Server Error
    """
    data = request.get_json()
    
    # 1. Bulletproof Error Handling: Dynamic Missing Field Check
    required_fields = ['enrollmentId', 'status']
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Bad Request. Missing required fields: {', '.join(missing)}"}), 400

    try:
        create_enrollment(data)
        return jsonify({"message": "Enrollment created successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/enrollment', methods=['GET'])
def get_all_enrollment_api():
    """
    Get all Enrollment records
    ---
    tags:
      - Enrollment
    responses:
      200:
        description: A list of Enrollment
      500:
        description: Internal Server Error
    """
    try:
        data = get_all_enrollment()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/enrollment/<int:id>', methods=['GET'])
def get_enrollment_api(id):
    """
    Get a specific Enrollment by ID
    ---
    tags:
      - Enrollment
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the Enrollment
    responses:
      200:
        description: Enrollment data returned
      404:
        description: Enrollment not found
    """
    try:
        data = get_enrollment_by_id(id)
        if data:
            return jsonify(data), 200
        return jsonify({"error": "Enrollment not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/enrollment/<int:id>', methods=['PUT'])
def update_enrollment_api(id):
    """
    Update an existing Enrollment
    ---
    tags:
      - Enrollment
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          id: EnrollmentUpdate
    responses:
      200:
        description: Enrollment updated
      404:
        description: Enrollment not found
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided to update"}), 400
        
    try:
        # Assuming your repo returns True/False or rows affected
        update_enrollment(id, data)
        return jsonify({"message": "Enrollment updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Update failed: {str(e)}"}), 500


@app.route('/enrollment/<int:id>', methods=['DELETE'])
def delete_enrollment_api(id):
    """
    Delete a Enrollment
    ---
    tags:
      - Enrollment
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Enrollment deleted
      404:
        description: Enrollment not found
    """
    try:
        delete_enrollment(id)
        return jsonify({"message": "Enrollment deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Delete failed: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(debug=True)